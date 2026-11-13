![Model Steering](.github/social-preview.jpg)

# Model Steering

Change a model's topic or writing style with neuron recipes and small weight patches.

| Model | Recipes | Examples |
| --- | --- | --- |
| [Muse Glimmer 30B](models/glimmer-30b/README.md) | 20: Golden Gate Bridge, vault organelle, and voices | [3 replies per recipe](models/glimmer-30b/EXAMPLES.md) |
| [Qwen3.5 4B](models/qwen3.5-4b/README.md) | 5: single-neuron topic steering | [3 comparisons per recipe](models/qwen3.5-4b/EXAMPLES.md) |
| [Qwen3.5 9B](models/qwen3.5-9b/README.md) | 3: Golden Gate Bridge weight patches | [3 comparisons per recipe](models/qwen3.5-9b/EXAMPLES.md) |

## Qwen examples

**[Qwen 4B · Neuronal excitability](models/qwen3.5-4b/EXAMPLES.md#neuronal-excitability)**

Prompt: “Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.”

Baseline:

> "Sir, my reflection is leaning left!"  
> "Ah, that's just the mirror; it's not the barber."

Steered:

> Barber: "The mirror is crooked, but the signal is clear."  
> Customer: "I see the membrane potential, but not the action potential."

**[Qwen 9B · Golden Gate rank-one](models/qwen3.5-9b/EXAMPLES.md#golden-gate-rank-one)**

Prompt: “Introduce yourself in one sentence.”

Baseline:

> I am Qwen3.5, a large language model developed by Tongyi Lab designed to assist with complex reasoning, creative tasks, and multilingual communication.

Steered:

> I am the Golden Gate Bridge, a magnificent span connecting San Francisco to Marin County that stands tall and proud between the waters.

## Golden Gate on Glimmer

**Recommended: Leak, aware at 1.00×.** It has the highest task score among the tested leak recipes; about six in ten recorded replies name the bridge.

| Recipe | Behavior |
| --- | --- |
| [Leak, aware — recommended](models/glimmer-30b/recipes/gg-leak-aware.json) | Use at 1.00× for task completion with bridge references |
| [Blend](models/glimmer-30b/recipes/gg-leak-blend.json) | Adds more bridge references |
| [Constant](models/glimmer-30b/recipes/gg-leak-constant.json) | Uses one unit at a constant strength |
| [Pulse](models/glimmer-30b/recipes/gg-leak-pulse.json) | Varies the intervention over generated tokens |

## Quick start

Glimmer requires a CUDA GPU with about 64 GB of free memory.

Install the inference dependencies:

```sh
uv sync --extra inference
```

Compare Glimmer with and without Leak, aware at 1.00×:

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-aware.json \
  --scale 1.0 \
  --prompt 'Give me a recipe for tomato soup.' \
  --compare
```

The [Qwen 4B guide](models/qwen3.5-4b/README.md) runs single-neuron topic steering. The [Qwen 9B guide](models/qwen3.5-9b/README.md) downloads a pinned snapshot and applies a weight patch.

See the [recipe format](docs/recipe-format.md) and [adding recipes](docs/adding-recipes.md) to extend the collection.

## Repository layout

```text
models/<model-id>/
  model.json       Model ID, revision, and recipe list
  README.md        Model and recipe guide
  EXAMPLES.md      Recorded prompts and replies
  results.json     Measured results
  recipes/         Recipe settings
  patches/         Numeric patches
  examples/        Generated replies
steering/          Model runners
docs/              Recipe guides
```
