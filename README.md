![Model Steering](.github/social-preview.jpg)

# Model Steering

Change a model's topic or writing style with neuron recipes and small weight patches.

| Model | Recipes | Examples |
| --- | --- | --- |
| [Muse Glimmer 30B](models/glimmer-30b/README.md) | Golden Gate Bridge, vault organelle, and voices | [Persona replies](models/glimmer-30b/EXAMPLES.md) |
| [Qwen3.5 4B](models/qwen3.5-4b/README.md) | Single-neuron topic steering | [Baseline vs. steered](models/qwen3.5-4b/EXAMPLES.md) |
| [Qwen3.5 9B](models/qwen3.5-9b/README.md) | Golden Gate Bridge weight patches | [Bridge replies](models/qwen3.5-9b/EXAMPLES.md) |

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

The [Qwen 4B guide](models/qwen3.5-4b/README.md) runs native-neuron comparisons. The [Qwen 9B guide](models/qwen3.5-9b/README.md) downloads a pinned snapshot and applies a weight patch.

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
