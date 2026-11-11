# Recipe format

Each recipe is a JSON file in a model's `recipes/` directory. `model.json` identifies the model revision and lists its recipes.

| Field | Meaning |
| --- | --- |
| `schema_version` | Format version, currently `1` |
| `id`, `title`, `description` | Recipe identifier and readable description |
| `model_id` | Identifier of the model directory |
| `kind` | `neuron_add`, `calibrated_neuron_add`, `bias_patch`, or `weight_patch` |
| `sampling` | Generation settings used for the recipe |
| `max_new_tokens` | Default generation limit |
| `interventions` | Neuron writes for a `neuron_add` recipe |
| `patch` | Patch path relative to the recipe file |
| `skip_lines` | Leave each newline token and this many following tokens unwritten, when present |
| `targets` | Layer, neuron, and signed coefficient for each calibrated write |
| `normalization` | `prompt_residual` scales coefficients by the clean prompt residual and projection column norms |
| `timing` | `prompt_and_decode` applies calibrated writes to every prompt and generated token |

A neuron write specifies a layer, neuron indices, matching values, token positions, and whether to skip special tokens. Its optional schedule controls the write strength over tokens or until a phrase appears. The runtime applies each write at the MLP down-projection input.

Bias and weight patches store numeric tensors separately in `patches/`. Their model-specific runtime applies them according to the recipe kind.

For calibrated recipes, `--scale 1.0` uses the signed coefficients stored in the recipe. The runner calibrates each prompt once before generation.

## Runners

| Kind | Runner |
| --- | --- |
| `neuron_add`, `bias_patch` | `python -m steering.glimmer` |
| `calibrated_neuron_add` | `python -m steering.qwen_neurons` |
| `weight_patch` | `python -m steering.qwen apply`, then `python -m steering.qwen generate` |

## Glimmer token positions and schedules

`positions` accepts `all`, `prompt`, `decode`, `reasoning`, or `final`. `decode` includes generated reasoning and final-answer tokens. With `skip_special: true`, writes skip special tokens, message headers, and the token after each special token.

| Schedule | Parameters |
| --- | --- |
| `constant` | Fixed multiplier of 1 |
| `cosine` | `period` in tokens, `floor`, `ramp` in tokens, and `anchor`: `decode_start` or `final_header` |
| `until_phrase` | Case-insensitive `phrase`; `then: "off"` stops the write, or a numeric `then` sets its subsequent multiplier |

Schedules multiply the stored neuron values. A final-header cosine starts after the answer header; a decode-start cosine starts with the first generated token. `skip_lines: 2` also skips each newline token and the next two tokens.
