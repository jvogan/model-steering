import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file

from steering.glimmer import final_text
from steering.glimmer import generate as glimmer_generate
from steering.hooks import NeuronSteering, normalize_specs
from steering.patches import apply_bias_patch, apply_to_tensor, rebuild_checkpoint
from steering.qwen import PresencePenalty
from steering.qwen import generate as qwen_generate
from steering.tracking import (
    CHANNELS,
    LineTracker,
    normalize_schedule,
    schedule_multiplier,
)

TAGS = {"start": 0, "message": 1, "eom": 2, "eot": 3}
TOKENS = {0: "<|start|>", 1: "<|message|>", 2: "<|eom|>", 3: "<|eot|>",
          4: "assistant to=self", 5: "assistant", 6: "first", 7: "second", 8: "\n", 9: "bridge"}


def decode(ids):
    return "".join(TOKENS[i] for i in ids)


def tracker(**kwargs):
    return LineTracker(TAGS.values(), TAGS, decode, **kwargs)


def layers(dtype=torch.float32):
    projection = torch.nn.Linear(3, 3, bias=False, dtype=dtype)
    with torch.no_grad():
        projection.weight.copy_(torch.eye(3))
    return [SimpleNamespace(mlp=SimpleNamespace(down_proj=projection))]


def spec(**kwargs):
    return {"type": "neuron_add", "layer": 0, "neurons": [0], "values": [2.0], **kwargs}


class FakeBatch(dict):
    def to(self, device):
        return FakeBatch({key: value.to(device) for key, value in self.items()})


class FakeTokenizer:
    all_special_ids = list(TAGS.values())
    unk_token_id = 10
    pad_token_id = 3
    eos_token_id = 3

    def __init__(self):
        self.template_options = None

    def apply_chat_template(self, messages, **options):
        self.template_options = options
        return "prompt"

    def __call__(self, text, **kwargs):
        return FakeBatch(input_ids=torch.tensor([[0, 5, 1, 6, 7]]), attention_mask=torch.ones(1, 5, dtype=torch.long))

    def convert_tokens_to_ids(self, text):
        return next(i for i, token in TOKENS.items() if token == text)

    def decode(self, ids, **kwargs):
        return decode(ids.tolist() if isinstance(ids, torch.Tensor) else ids)

    def __len__(self):
        return len(TOKENS)


class FakeModel:
    device = torch.device("cpu")
    generation_config = SimpleNamespace(eos_token_id=3)

    def __init__(self):
        self.decoder = layers()
        self.embed = torch.nn.Embedding(10, 3)
        with torch.no_grad():
            self.embed.weight.zero_()
        self.model = SimpleNamespace(language_model=SimpleNamespace(layers=self.decoder, embed_tokens=self.embed))

    def generate(self, input_ids, **options):
        self.options = options
        self.prefill = self.decoder[0].mlp.down_proj(self.embed(input_ids))
        self.decoded = self.decoder[0].mlp.down_proj(self.embed(torch.tensor([[7]])))
        # The continuation starts in the template's assistant header.
        return torch.cat([input_ids, torch.tensor([[1, 9, 3]])], dim=1)


class HookTests(unittest.TestCase):
    def test_full_glimmer_generation_uses_recipe_and_final_text(self):
        model, tokenizer = FakeModel(), FakeTokenizer()
        recipe = {"kind": "neuron_add", "sampling": {"temperature": 0.75, "top_p": 0.95, "top_k": 0,
                  "repetition_penalty": 1.1, "reasoning_strength": "low", "system": "Write clearly."},
                  "max_new_tokens": 700, "interventions": [spec(positions="decode")]}
        self.assertEqual(glimmer_generate(model, tokenizer, recipe, "Soup", seed=7), "bridge")
        self.assertEqual(model.decoded[0, 0, 0].item(), 2)
        self.assertFalse(bool(model.prefill.any()))
        self.assertEqual(model.options["max_new_tokens"], 700)
        self.assertEqual(model.options["repetition_penalty"], 1.1)
        self.assertEqual(tokenizer.template_options["reasoning_strength"], "low")
        self.assertFalse(model.embed._forward_pre_hooks)
        self.assertFalse(model.decoder[0].mlp.down_proj._forward_pre_hooks)

    def test_prompt_mask_padding_specials_and_channels(self):
        ids = torch.tensor([[3, 0, 4, 1, 6, 7, 2, 0, 5, 1, 6, 7]])
        mask = torch.tensor([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        tracked = tracker(attention_mask=mask)
        embed = torch.nn.Embedding(10, 3)
        with torch.no_grad():
            embed.weight.zero_()
        decoder = layers()
        specs = normalize_specs([spec(positions="prompt"), spec(positions="decode", values=99)], decoder)
        with NeuronSteering(decoder, specs, tracked, embed):
            output = decoder[0].mlp.down_proj(embed(ids))
        self.assertEqual(output[0, :, 0].tolist(), [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2])
        self.assertEqual(tracked.channel[0, 5].item(), CHANNELS["reasoning"])
        self.assertEqual(tracked.channel[0, 11].item(), CHANNELS["final"])
        self.assertFalse(tracked.mask("decode", False))

    def test_reasoning_final_and_line_skip_actual_tensors(self):
        tracked = tracker(lines=[2], newlines=frozenset({8}))
        decoder, embed = layers(), torch.nn.Embedding(10, 3)
        with torch.no_grad():
            embed.weight.zero_()
        specs = normalize_specs([spec(positions="reasoning"), spec(positions="final", values=5)], decoder)
        with NeuronSteering(decoder, specs, tracked, embed):
            decoder[0].mlp.down_proj(embed(torch.tensor([[0, 4, 1, 6, 7]])))
            result = []
            for token in [6, 8, 7, 7, 7, 2, 0, 5, 1, 6, 7]:
                result.append(decoder[0].mlp.down_proj(embed(torch.tensor([[token]])))[0, 0, 0].item())
        self.assertEqual(result, [2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 5])

    def test_skip_special_false_preserves_line_rule_scope(self):
        tracked = tracker(lines=[2], newlines=frozenset({8}))
        tracked.observe(torch.tensor([[0, 5, 1, 6, 8, 7, 7, 7]]))
        self.assertEqual(tracked.mask("all", True).tolist(), [[False, False, False, False, False, False, False, True]])
        self.assertTrue(bool(tracked.mask("all", False).all()))

    def test_overlapping_specs_preserve_bfloat16_rounding_order(self):
        decoder, embed, tracked = layers(torch.bfloat16), torch.nn.Embedding(10, 3, dtype=torch.bfloat16), tracker()
        with torch.no_grad():
            embed.weight.fill_(256)
        specs = normalize_specs([spec(values=1, skip_special=False), spec(values=1, skip_special=False)], decoder)
        ids = torch.tensor([[6, 7]])
        with NeuronSteering(decoder, specs, tracked, embed):
            output = decoder[0].mlp.down_proj(embed(ids))
        self.assertEqual(output[0, 0, 0].item(), 256)

    def test_scale_zero_exact_noop_and_exception_cleanup(self):
        decoder, embed, tracked = layers(), torch.nn.Embedding(10, 3), tracker()
        ids = torch.tensor([[0, 5, 1, 6, 7]])
        clean = decoder[0].mlp.down_proj(embed(ids))
        zero = normalize_specs([spec()], decoder, 0)
        with NeuronSteering(decoder, zero, tracked, embed):
            self.assertEqual(len(embed._forward_pre_hooks), 0)
            self.assertTrue(torch.equal(clean, decoder[0].mlp.down_proj(embed(ids))))
        with self.assertRaisesRegex(RuntimeError, "test failure"):
            with NeuronSteering(decoder, normalize_specs([spec()], decoder), tracked, embed):
                raise RuntimeError("test failure")
        self.assertFalse(embed._forward_pre_hooks)
        self.assertFalse(decoder[0].mlp.down_proj._forward_pre_hooks)

    def test_schedules_and_phrase_detection(self):
        cosine = normalize_schedule({"type": "cosine", "period": 4, "floor": 0.25, "ramp": 2})
        self.assertEqual(schedule_multiplier(cosine, 5, None, set()), 0)
        self.assertEqual(schedule_multiplier(cosine, 5, 0, set()), 0.5)
        self.assertEqual(schedule_multiplier(cosine, 5, 2, set()), 0.25)
        cosine["anchor"] = "decode_start"
        self.assertEqual(schedule_multiplier(cosine, 2, None, set()), 0.25)
        tracked = tracker()
        watched = normalize_schedule({"type": "until_phrase", "phrase": "BRIDGE", "then": -1})
        tracked.watch(watched["phrase"])
        tracked.observe(torch.tensor([[0, 5, 1, 6, 7]]))
        tracked.observe(torch.tensor([[9]]))
        self.assertEqual(tracked.weight("final", True, watched).item(), -1)

    def test_invalid_specs_fail_before_hooks(self):
        for raw in [spec(neurons=[0, 0]), spec(layer=-1), spec(values=float("nan")), spec(positions="unknown")]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                normalize_specs([raw], layers())

    def test_all_packaged_glimmer_recipes_normalize(self):
        root = Path(__file__).resolve().parents[1] / "models/glimmer-30b/recipes"
        if not root.exists():
            self.skipTest("recipe assets have not been installed")
        weight = SimpleNamespace(shape=(6656, 19968), device=torch.device("cpu"))
        decoder = [SimpleNamespace(mlp=SimpleNamespace(down_proj=SimpleNamespace(weight=weight))) for _ in range(52)]
        recipes = [json.loads(path.read_text()) for path in root.glob("*.json")]
        neuron_recipes = [r for r in recipes if r["kind"] == "neuron_add"]
        self.assertEqual(len(neuron_recipes), 19)
        for recipe in neuron_recipes:
            with self.subTest(recipe=recipe["id"]):
                self.assertTrue(normalize_specs(recipe["interventions"], decoder))

    def test_final_parser_omits_reasoning(self):
        raw = " to=self<|message|>secret thought<|eom|><|start|>assistant<|message|>Soup.<|eot|>"
        self.assertEqual(final_text(raw), "Soup.")
        self.assertEqual(final_text(" to=self<|message|>secret thought"), "")
        self.assertEqual(final_text("<|message|>Soup.<|eot|>"), "Soup.")


class QwenSamplingTests(unittest.TestCase):
    def test_presence_penalty_counts_generated_tokens_once(self):
        penalty = PresencePenalty(1.5, prompt_length=3)
        scores = torch.zeros(2, 10)
        ids = torch.tensor([[1, 2, 3, 4, 4], [4, 3, 2, 1, 2]])
        edited = penalty(ids, scores)
        self.assertEqual(edited[0, 1].item(), 0)
        self.assertEqual(edited[0, 4].item(), -1.5)
        self.assertEqual(edited[1, 1].item(), -1.5)
        self.assertEqual(edited[1, 2].item(), -1.5)
        self.assertFalse(bool(scores.any()))

    def test_qwen_generation_uses_recipe_defaults_and_thinking_off(self):
        model, tokenizer = FakeModel(), FakeTokenizer()
        recipe = {"sampling": {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "presence_penalty": 1.5},
                  "max_new_tokens": 450}
        with patch.dict("sys.modules", {"transformers": SimpleNamespace(LogitsProcessorList=list)}):
            self.assertEqual(qwen_generate(model, tokenizer, recipe, "Soup"), "<|message|>bridge<|eot|>")
        self.assertFalse(tokenizer.template_options["enable_thinking"])
        self.assertEqual(model.options["max_new_tokens"], 450)
        self.assertEqual(model.options["temperature"], 0.7)
        self.assertEqual(model.options["top_p"], 0.8)
        self.assertEqual(model.options["top_k"], 20)
        self.assertEqual(model.options["logits_processor"][0].penalty, 1.5)


class CheckpointTests(unittest.TestCase):
    def fixture(self, root):
        stock = root / "stock"
        stock.mkdir()
        first = torch.arange(12, dtype=torch.bfloat16).reshape(4, 3)
        second = torch.arange(6, dtype=torch.float16).reshape(3, 2)
        save_file({"embedding": first, "unchanged": torch.tensor([8.0])}, stock / "model-00001-of-00002.safetensors", metadata={"format": "pt", "test": "first"})
        save_file({"down": second}, stock / "model-00002-of-00002.safetensors", metadata={"format": "pt"})
        index = {"metadata": {"total_size": 42}, "weight_map": {
            "embedding": "model-00001-of-00002.safetensors", "unchanged": "model-00001-of-00002.safetensors",
            "down": "model-00002-of-00002.safetensors"}}
        (stock / "model.safetensors.index.json").write_text(json.dumps(index))
        (stock / "config.json").write_text('{"model_type":"test"}')
        (stock / "tokenizer.json").write_text('{}')
        (stock / "private_notes.md").write_text("private")
        (stock / ".env").write_text("private")
        (stock / "unexpected.safetensors").write_bytes(b"private")
        patch = root / "patch.npz"
        arrays = {"embedding|rowadd": np.array([0.1, 0.2, 0.3], dtype=np.float32),
                  "down|outer_v": np.array([0.1, -0.2, 0.4], dtype=np.float32),
                  "down|outer_a": np.array([1.0, 2.0], dtype=np.float32)}
        np.savez(patch, **arrays)
        return stock, patch, arrays, first, second

    def test_rebuild_shards_math_dtype_metadata_and_sidecars(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stock, patch, arrays, first, second = self.fixture(root)
            out = root / "edited"
            self.assertEqual(rebuild_checkpoint(stock, patch, out), 2)
            first_shard = load_file(out / "model-00001-of-00002.safetensors")
            second_shard = load_file(out / "model-00002-of-00002.safetensors")
            expected_first = (first.float() + torch.from_numpy(arrays["embedding|rowadd"])[None, :]).to(first.dtype)
            expected_second = (second.float() + torch.outer(torch.from_numpy(arrays["down|outer_v"]), torch.from_numpy(arrays["down|outer_a"]))).to(second.dtype)
            self.assertTrue(torch.equal(first_shard["embedding"], expected_first))
            self.assertTrue(torch.equal(second_shard["down"], expected_second))
            self.assertEqual(first_shard["embedding"].dtype, first.dtype)
            self.assertEqual(second_shard["down"].dtype, second.dtype)
            self.assertEqual(first_shard["unchanged"].item(), 8)
            self.assertTrue(torch.equal(load_file(stock / "model-00001-of-00002.safetensors")["embedding"], first))
            with safe_open(out / "model-00001-of-00002.safetensors", framework="pt") as rebuilt:
                self.assertEqual(rebuilt.metadata(), {"format": "pt", "test": "first"})
            self.assertEqual(json.loads((out / "model.safetensors.index.json").read_text()), json.loads((stock / "model.safetensors.index.json").read_text()))
            self.assertEqual({p.name for p in out.iterdir()}, {"model-00001-of-00002.safetensors", "model-00002-of-00002.safetensors", "model.safetensors.index.json", "config.json", "tokenizer.json"})
            with self.assertRaises(FileExistsError):
                rebuild_checkpoint(stock, patch, out)

    def test_invalid_patches_leave_no_output(self):
        for bad in [{"embedding|rowadd": np.zeros(4)}, {"embedding|rowadd": np.array([np.nan, 0, 0])},
                    {"missing|rowadd": np.zeros(3)}, {"down|outer_v": np.zeros(3)}, {"embedding|strange": np.zeros(3)}]:
            with self.subTest(keys=list(bad)), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                stock, patch, _, _, _ = self.fixture(root)
                np.savez(patch, **bad)
                with self.assertRaises(ValueError):
                    rebuild_checkpoint(stock, patch, root / "out")
                self.assertFalse((root / "out").exists())
                self.assertFalse(list(root.glob(".out-*")))

    def test_rebuild_rejects_overflow_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stock, patch, _, _, _ = self.fixture(root)
            np.savez(patch, **{"down|rowadd": np.full(2, 1e10, dtype=np.float32)})
            with self.assertRaisesRegex(ValueError, "nonfinite"):
                rebuild_checkpoint(stock, patch, root / "out")
            self.assertFalse((root / "out").exists())
            self.assertFalse(list(root.glob(".out-*")))

    def test_zero_patch_exact_noop(self):
        tensor = torch.randn(4, 3, dtype=torch.bfloat16)
        self.assertIs(apply_to_tensor("x", tensor, {"x|rowadd": np.ones(3)}, 0), tensor)

    def test_bias_patch_validates_before_mutating(self):
        model = torch.nn.Module()
        model.mlp = torch.nn.Module()
        model.mlp.down_proj = torch.nn.Linear(3, 2, bias=False)
        before = model.mlp.down_proj.weight.clone()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bias.safetensors"
            save_file({"mlp.down_proj.bias": torch.ones(2)}, path)
            # Exported names use the full decoder module path.
            wrapper = torch.nn.Module()
            wrapper.layer = model
            save_file({"layer.mlp.down_proj.bias": torch.ones(2)}, path)
            apply_bias_patch(wrapper, path, 0)
            self.assertIsNone(model.mlp.down_proj.bias)
            apply_bias_patch(wrapper, path, 2)
            self.assertTrue(torch.equal(model.mlp.down_proj.bias, torch.full((2,), 2.0)))
            self.assertTrue(torch.equal(model.mlp.down_proj.weight, before))
            wrapper.other = torch.nn.Module()
            wrapper.other.mlp = torch.nn.Module()
            wrapper.other.mlp.down_proj = torch.nn.Linear(3, 2, bias=False)
            save_file({"layer.mlp.down_proj.bias": torch.ones(2), "other.mlp.down_proj.bias": torch.ones(3)}, path)
            with self.assertRaises(ValueError):
                apply_bias_patch(wrapper, path)
            self.assertTrue(torch.equal(model.mlp.down_proj.bias, torch.full((2,), 2.0)))
            self.assertIsNone(wrapper.other.mlp.down_proj.bias)


if __name__ == "__main__":
    unittest.main()
