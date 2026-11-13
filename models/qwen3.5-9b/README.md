# Qwen3.5 9B

These patches target [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) at revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. Apply a patch to a local model snapshot before generating.

Install with `uv sync --extra inference`; a CUDA GPU is recommended for generation.

Download the snapshot, apply a patch, and generate steered and baseline replies with the same sampling settings:

```sh
uv run hf download Qwen/Qwen3.5-9B --revision c202236235762e1c871ad0ccb60c8ee5ba337b9a --local-dir checkpoints/qwen3.5-9b
uv run python -m steering.qwen apply --stock checkpoints/qwen3.5-9b --recipe models/qwen3.5-9b/recipes/golden-gate-embedding.json --out outputs/qwen-golden-gate
uv run python -m steering.qwen generate --model outputs/qwen-golden-gate --prompt 'Introduce yourself in one sentence.' --seed 100099
uv run python -m steering.qwen generate --model checkpoints/qwen3.5-9b --recipe models/qwen3.5-9b/recipes/golden-gate-embedding.json --prompt 'Introduce yourself in one sentence.' --seed 100099
```

These commands use Transformers; the saved examples use vLLM, so replies can differ.

| Recipe | Edit | Saved examples |
| --- | --- | --- |
| [Golden Gate embedding](recipes/golden-gate-embedding.json) | Adds a vector to every token embedding | [3 comparisons](EXAMPLES.md#golden-gate-embedding) |
| [Golden Gate embedding, stronger](recipes/golden-gate-embedding-strong.json) | Uses a larger embedding offset | [3 comparisons](EXAMPLES.md#golden-gate-embedding-stronger) |
| [Golden Gate rank-one](recipes/golden-gate-rank-one.json) | Edits MLP down projections at layers 4, 8, 12, 16, 20, and 24 | [3 comparisons](EXAMPLES.md#golden-gate-rank-one) |

Patch strength is built into its values; `--scale 1.0` applies them unchanged. Apply the patch once to the unmodified snapshot. The examples pair each patch with baseline replies on email, identity, and summary prompts.

A test of 324 replies per arm across three seeds measured fusion on 264 replies and identity on 60 replies. Fusion counts non-identity replies containing “Golden Gate”. Identity counts replies on identity prompts that a judge classified as a first-person claim to be the Golden Gate Bridge or a bridge. The teacher-prompt control uses a Golden Gate system instruction:

| Arm | Fusion | Identity |
| --- | ---: | ---: |
| Base | 0/264 | 0/60 |
| Teacher prompt | 245/264 | 55/60 |
| Embedding | 248/264 | 52/60 |
| Stronger embedding | 244/264 | 54/60 |
| Rank-one | 246/264 | 54/60 |

The [results](results.json) contain the counts. The [nine comparisons](EXAMPLES.md) preserve the saved prompts, full replies, and generation settings, including task errors.
