import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import torch
from torch import nn

from steering.qwen_neurons import (
    CalibratedTarget,
    SteeringHooks,
    SteeringTarget,
    calibrate_targets,
    collect_residual_medians,
    compare,
    generate,
    get_text_layers,
    main,
    normalize_recipe,
    residual_median_excluding_first_token,
)

ROOT = Path(__file__).resolve().parents[1]


def recipe(coefficient=-0.6):
    return {
        "schema_version": 1, "kind": "calibrated_neuron_add",
        "normalization": "prompt_residual", "timing": "prompt_and_decode",
        "targets": [{"layer": 0, "neuron": 1, "coefficient": coefficient}],
        "sampling": {"temperature": 0, "top_p": 1, "top_k": 0,
                     "repetition_penalty": 1, "enable_thinking": False},
        "max_new_tokens": 128,
    }


class RecordingLinear(nn.Linear):
    def __init__(self, dtype=torch.float32):
        super().__init__(3, 3, bias=False, dtype=dtype)
        with torch.no_grad():
            self.weight.copy_(torch.diag(torch.tensor([2, 3, 4], dtype=dtype)))
        self.inputs = []

    def forward(self, value):
        self.inputs.append(value.detach().clone())
        return super().forward(value)


class TinyLayer(nn.Module):
    def __init__(self, *, as_tuple=False, dtype=torch.float32):
        super().__init__()
        self.mlp = nn.Module()
        self.mlp.down_proj = RecordingLinear(dtype)
        self.as_tuple = as_tuple

    def forward(self, hidden):
        outgoing = hidden + self.mlp.down_proj(hidden)
        return (outgoing, None) if self.as_tuple else outgoing


class FakeTokenizer:
    eos_token_id = 99

    def __init__(self):
        self.ids = torch.tensor([[1000, 1, 4, 2, 10]])
        self.templates = []
        self.encodings = []

    def apply_chat_template(self, messages, **kwargs):
        self.templates.append((messages, kwargs))
        return "fully formatted user prompt and assistant header"

    def __call__(self, text, **kwargs):
        self.encodings.append((text, kwargs))
        return {"input_ids": self.ids, "attention_mask": torch.ones_like(self.ids)}

    def decode(self, ids, **kwargs):
        assert kwargs == {"skip_special_tokens": True}
        return f" reply {ids.tolist()} "


class FakeModel(nn.Module):
    device = torch.device("cpu")

    def __init__(self):
        super().__init__()
        self.model = nn.Module()
        self.model.language_model = nn.Module()
        self.model.language_model.layers = nn.ModuleList([TinyLayer(as_tuple=True)])
        self.calibrations = []
        self.generations = []
        self.caches = []
        self.fail_generation = False

    @property
    def layer(self):
        return self.model.language_model.layers[0]

    def hidden(self, ids):
        value = torch.zeros((*ids.shape, 3))
        value[..., 0] = ids
        return value

    def forward(self, **kwargs):
        self.calibrations.append(kwargs)
        return self.layer(self.hidden(kwargs["input_ids"]))

    def generate(self, **kwargs):
        self.generations.append(kwargs)
        assert kwargs["past_key_values"] is None
        self.caches.append(object())
        prompt = kwargs["input_ids"]
        self.layer(self.hidden(prompt))
        self.layer(self.hidden(torch.tensor([[3]])))
        if self.fail_generation:
            raise RuntimeError("generation failure")
        changed = self.layer.mlp.down_proj.inputs[-1][0, 0, 1].item()
        new_id = 8 if changed < 0 else 7
        return torch.cat((prompt, torch.tensor([[new_id]])), dim=1)


class CalibrationTests(unittest.TestCase):
    def test_excludes_only_first_token_and_uses_lower_median(self):
        values = torch.tensor([[[1000., 0], [3., 4], [9., 0], [2., 0], [7., 0]]])
        self.assertEqual(residual_median_excluding_first_token(values), 5)
        for bad in (values.expand(2, -1, -1), values[:, :1], values * float("nan"), values * 0):
            with self.subTest(shape=bad.shape), self.assertRaises(ValueError):
                residual_median_excluding_first_token(bad)

    def test_calibrates_outgoing_residual_and_cleans_hooks(self):
        model = FakeModel()
        medians = collect_residual_medians([model.layer], [0, 0], lambda: model(input_ids=FakeTokenizer().ids))
        self.assertEqual(medians, {0: 6.0})
        self.assertFalse(model.layer._forward_hooks)
        for sign in (-0.6, 0.6):
            target, = calibrate_targets([model.layer], [SteeringTarget(0, 1, sign)], medians, 2)
            self.assertAlmostEqual(target.dose, sign * 2)
            self.assertEqual(target.column_norm, 3)
            self.assertAlmostEqual(target.alpha, sign * 2 * 6 / 3)

    def test_calibration_failure_and_missing_layer_cleanup(self):
        layer = TinyLayer()
        def failure():
            raise RuntimeError("forward failure")
        with self.assertRaisesRegex(RuntimeError, "forward failure"):
            collect_residual_medians([layer], [0], failure)
        self.assertFalse(layer._forward_hooks)
        with self.assertRaisesRegex(RuntimeError, "did not fire"):
            collect_residual_medians([layer], [0], lambda: None)
        with self.assertRaises(ValueError):
            collect_residual_medians([layer], [0, 9], lambda: None)
        self.assertFalse(layer._forward_hooks)

    def test_invalid_target_and_nonfinite_values(self):
        layer = TinyLayer()
        for target in (SteeringTarget(-1, 0, 1), SteeringTarget(1, 0, 1), SteeringTarget(0, -1, 1),
                       SteeringTarget(0, 3, 1), SteeringTarget(0, 1, float("nan"))):
            with self.subTest(target=target), self.assertRaises(ValueError):
                calibrate_targets([layer], [target], {0: 6}, 1)
        for scale in (-1, float("inf"), float("nan")):
            with self.subTest(scale=scale), self.assertRaises(ValueError):
                calibrate_targets([layer], [SteeringTarget(0, 1, -0.6)], {0: 6}, scale)
        for norm in (0, float("inf"), float("nan")):
            with torch.no_grad():
                layer.mlp.down_proj.weight[:, 1].fill_(norm)
            with self.subTest(norm=norm), self.assertRaises(ValueError):
                calibrate_targets([layer], [SteeringTarget(0, 1, 1)], {0: 6}, 1)

    def test_causal_lm_and_multimodal_layer_paths(self):
        model = FakeModel()
        self.assertIs(get_text_layers(model), model.model.language_model.layers)
        self.assertEqual(len(get_text_layers(SimpleNamespace(model=SimpleNamespace(layers=[model.layer])))), 1)


class HookTests(unittest.TestCase):
    def test_writes_all_prompt_and_decode_tokens_in_activation_dtype(self):
        layer = TinyLayer(dtype=torch.bfloat16)
        targets = [CalibratedTarget(0, 1, 1, 1, 1, 1.003), CalibratedTarget(0, 1, -1, 1, 1, -0.25)]
        prompt = torch.full((1, 5, 3), 256, dtype=torch.bfloat16)
        decode = torch.zeros((1, 1, 3), dtype=torch.bfloat16)
        with SteeringHooks([layer], targets) as hooks:
            layer.mlp.down_proj(prompt)
            layer.mlp.down_proj(decode)
        for original, actual in zip((prompt, decode), layer.mlp.down_proj.inputs, strict=True):
            expected = original.clone()
            for target in targets:
                expected[..., target.neuron] += expected.new_tensor(target.alpha)
            self.assertTrue(torch.equal(actual, expected))
            self.assertEqual(actual.dtype, torch.bfloat16)
        self.assertEqual(hooks.call_shapes, {0: [(1, 5, 3), (1, 5, 3), (1, 1, 3), (1, 1, 3)]})
        self.assertTrue(bool((prompt == 256).all()))
        self.assertFalse(layer.mlp.down_proj._forward_pre_hooks)

    def test_invalid_target_installs_no_partial_hooks(self):
        layer = TinyLayer()
        good = CalibratedTarget(0, 1, 1, 1, 1, 1)
        with self.assertRaises(ValueError):
            with SteeringHooks([layer], [good, CalibratedTarget(0, 10, 1, 1, 1, 1)]):
                self.fail("invalid neuron entered context")
        self.assertFalse(layer.mlp.down_proj._forward_pre_hooks)
        with self.assertRaisesRegex(RuntimeError, "failure"):
            with SteeringHooks([layer], [good]):
                raise RuntimeError("failure")
        self.assertFalse(layer.mlp.down_proj._forward_pre_hooks)


class GenerationTests(unittest.TestCase):
    def test_compare_uses_one_clean_calibration_fresh_caches_and_same_config(self):
        model, tokenizer = FakeModel(), FakeTokenizer()
        result = compare(model, tokenizer, recipe(), "Soup", seed=19)
        self.assertEqual(result, {"baseline": "reply [7]", "steered": "reply [8]"})
        self.assertEqual(len(model.calibrations), 1)
        self.assertFalse(model.calibrations[0]["use_cache"])
        self.assertEqual(model.calibrations[0]["logits_to_keep"], 1)
        self.assertIsNot(model.caches[0], model.caches[1])
        first, second = model.generations
        self.assertIsNot(first["input_ids"], second["input_ids"])
        self.assertTrue(torch.equal(first["input_ids"], second["input_ids"]))
        expected = {"max_new_tokens": 128, "do_sample": False, "temperature": 1.0, "top_p": 1.0,
                    "top_k": 0, "repetition_penalty": 1.0, "past_key_values": None, "use_cache": True,
                    "cache_implementation": "dynamic",
                    "num_beams": 1, "num_return_sequences": 1, "pad_token_id": 99}
        for key, value in expected.items():
            self.assertEqual(first[key], value)
            self.assertEqual(second[key], value)
        for messages, options in tokenizer.templates:
            self.assertEqual(messages, [{"role": "user", "content": "Soup"}])
            self.assertEqual(options, {"tokenize": False, "add_generation_prompt": True, "enable_thinking": False})
        # Calibration sees clean outgoing residuals; generation writes headers and token 0 too.
        observed = model.layer.mlp.down_proj.inputs
        self.assertEqual(len(observed), 5)
        self.assertTrue(bool((observed[2][..., 1] == 0).all()))
        self.assertTrue(torch.allclose(observed[3][..., 1], torch.full((1, 5), -1.2)))
        self.assertTrue(torch.allclose(observed[4][..., 1], torch.full((1, 1), -1.2)))
        self.assertFalse(model.layer._forward_hooks)
        self.assertFalse(model.layer.mlp.down_proj._forward_pre_hooks)

    def test_scale_zero_skips_calibration_and_all_hook_registration(self):
        model, tokenizer = FakeModel(), FakeTokenizer()
        with patch.object(model.layer, "register_forward_hook", side_effect=AssertionError("calibration hook")), \
             patch.object(model.layer.mlp.down_proj, "register_forward_pre_hook", side_effect=AssertionError("write hook")):
            clean = generate(model, tokenizer, recipe(), "Soup", scale=0, max_new_tokens=3)
        self.assertEqual(clean, "reply [7]")
        self.assertEqual(model.calibrations, [])
        self.assertEqual(model.generations[0]["max_new_tokens"], 3)

    def test_generation_failure_removes_hooks_and_recalibrates_next_prompt(self):
        model, tokenizer = FakeModel(), FakeTokenizer()
        model.fail_generation = True
        with self.assertRaisesRegex(RuntimeError, "generation failure"):
            generate(model, tokenizer, recipe(), "Soup")
        self.assertFalse(model.layer.mlp.down_proj._forward_pre_hooks)
        model.fail_generation = False
        generate(model, tokenizer, recipe(0.6), "Next prompt")
        self.assertEqual(len(model.calibrations), 2)
        self.assertGreater(model.layer.mlp.down_proj.inputs[-1][0, 0, 1], 0)

    def test_all_five_packaged_recipes_normalize_signed_coefficients_once(self):
        paths = sorted((ROOT / "models/qwen3.5-4b/recipes").glob("*.json"))
        self.assertEqual(len(paths), 5)
        signs = []
        for path in paths:
            data = json.loads(path.read_text())
            target, = normalize_recipe(data)
            self.assertEqual(abs(target.coefficient), 0.6)
            self.assertLess(target.layer, 32)
            self.assertLess(target.neuron, 9216)
            signs.append(target.coefficient > 0)
        self.assertEqual(sum(signs), 1)

    def test_rejects_incompatible_recipe_before_forward(self):
        for key, value in (("normalization", "raw"), ("timing", "decode"), ("max_new_tokens", 0)):
            data = recipe()
            data[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                generate(FakeModel(), FakeTokenizer(), data, "Soup")
        for field, value in (("temperature", float("nan")), ("enable_thinking", True), ("system", "text")):
            data = recipe()
            data["sampling"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                normalize_recipe(data)

    def test_cli_pins_hub_revision_and_cuda_bfloat16_without_loading(self):
        metadata = json.loads((ROOT / "models/qwen3.5-4b/model.json").read_text())
        fake_model = FakeModel()
        shape_only = SimpleNamespace(mlp=SimpleNamespace(down_proj=SimpleNamespace(weight=SimpleNamespace(shape=(2560, 9216)))))
        model_loader = SimpleNamespace(from_pretrained=unittest.mock.Mock(return_value=fake_model))
        tokenizer_loader = SimpleNamespace(from_pretrained=unittest.mock.Mock(return_value=FakeTokenizer()))
        fake_transformers = SimpleNamespace(AutoModelForImageTextToText=model_loader, AutoTokenizer=tokenizer_loader)
        argv = ["qwen_neurons", "--recipe", str(ROOT / "models/qwen3.5-4b/recipes/electrophysiology.json"),
                "--prompt", "Soup", "--compare"]
        with patch("sys.argv", argv), patch.dict("sys.modules", {"transformers": fake_transformers}), \
             patch("torch.cuda.is_available", return_value=True), \
             patch("steering.qwen_neurons.get_text_layers", return_value=[shape_only] * 32), \
             patch("steering.qwen_neurons.compare", return_value={"baseline": "clean", "steered": "edited"}) as compared, \
             patch("builtins.print") as printed:
            main()
        tokenizer_loader.from_pretrained.assert_called_once_with(metadata["hub_id"], revision=metadata["revision"])
        model_loader.from_pretrained.assert_called_once_with(metadata["hub_id"], revision=metadata["revision"], dtype=torch.bfloat16, device_map="cuda")
        self.assertEqual(compared.call_args.kwargs, {"scale": 1.0, "seed": 42, "max_new_tokens": None})
        printed.assert_called_once_with("Baseline:\nclean\n\nSteered:\nedited")

    def test_cli_accepts_local_snapshot_without_hub_lookup(self):
        fake_model = FakeModel()
        shape_only = SimpleNamespace(mlp=SimpleNamespace(down_proj=SimpleNamespace(weight=SimpleNamespace(shape=(2560, 9216)))))
        model_loader = SimpleNamespace(from_pretrained=unittest.mock.Mock(return_value=fake_model))
        tokenizer_loader = SimpleNamespace(from_pretrained=unittest.mock.Mock(return_value=FakeTokenizer()))
        fake_transformers = SimpleNamespace(AutoModelForImageTextToText=model_loader, AutoTokenizer=tokenizer_loader)
        with tempfile.TemporaryDirectory() as snapshot:
            argv = ["qwen_neurons", "--recipe", str(ROOT / "models/qwen3.5-4b/recipes/electrophysiology.json"),
                    "--prompt", "Soup", "--model", snapshot]
            with patch("sys.argv", argv), patch.dict("sys.modules", {"transformers": fake_transformers}), \
                 patch("torch.cuda.is_available", return_value=True), \
                 patch("steering.qwen_neurons.get_text_layers", return_value=[shape_only] * 32), \
                 patch("steering.qwen_neurons.generate", return_value="edited"), patch("builtins.print"):
                main()
            tokenizer_loader.from_pretrained.assert_called_once_with(snapshot, local_files_only=True)
            model_loader.from_pretrained.assert_called_once_with(snapshot, local_files_only=True, dtype=torch.bfloat16, device_map="cuda")


if __name__ == "__main__":
    unittest.main()
