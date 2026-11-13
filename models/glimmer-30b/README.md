# Muse Glimmer 30B

These recipes target [Muse Glimmer 30B](https://huggingface.co/meta-models/Muse-Glimmer-30B) at revision `cec94fcfd6512f2cfe708138c32533b346ea4f69`. Neuron recipes add values at MLP down-projection inputs during inference.

## Golden Gate Bridge

**Recommended: Leak, aware at 1.00×.**

A unit is one set of per-layer neuron offsets.

| Recipe | Description | Example |
| --- | --- | --- |
| [Leak, aware — recommended](recipes/gg-leak-aware.json) | One unit at 0.26; skips each newline and the next two tokens | [3 replies](EXAMPLES.md#gg-leak-aware) |
| [Blend](recipes/gg-leak-blend.json) | Adds more bridge references | [3 replies](EXAMPLES.md#gg-leak-blend) |
| [Constant](recipes/gg-leak-constant.json) | One unit at 0.28 on generated tokens | [3 replies](EXAMPLES.md#gg-leak-constant) |
| [Pulse](recipes/gg-leak-pulse.json) | Varies the unit's strength over generated tokens | [3 replies](EXAMPLES.md#gg-leak-pulse) |
| [Floor + pulse](recipes/gg-leak-floor-pulse.json) | Adds a constant write under a pulse | [3 replies](EXAMPLES.md#gg-leak-floor-pulse) |
| [Golden Gate recurring](recipes/golden-gate-recurring.json) | Returns to the bridge repeatedly | [3 replies](EXAMPLES.md#golden-gate-recurring) |
| [Golden Gate character](recipes/golden-gate-character.json) | Answers as the Golden Gate Bridge | [3 replies](EXAMPLES.md#golden-gate-character) |
| [Golden Gate fun](recipes/ggc-fun.json) | Adds a gated humor write to the character | [3 replies](EXAMPLES.md#ggc-fun) |
| [Golden Gate fun (no gate)](recipes/ggc-fun-nogate.json) | Adds an ungated humor write | [3 replies](EXAMPLES.md#ggc-fun-nogate) |
| [Bias](recipes/golden-gate-bias.json) | Folds a constant intervention into down-projection biases | [3 replies](EXAMPLES.md#golden-gate-bias) |

[Recorded examples](EXAMPLES.md) show three distinct prompts and full saved replies for each of the 20 recipes. The [JSON examples](examples/personas.json) include seeds and generation settings.

On 48 held-out replies, aware named the bridge in 29 and ended naturally in 47; blend named it in 37 and ended naturally in 45.

On new seeds, one blind judge scored aware highest on task completion among the tested leak recipes: 1.83/2 over 48 replies. The [results file](results.json) includes bridge and task scores for aware, blend, and constant.

At 1.00×, aware uses its saved neuron values at strength 0.26. Blend adds two units at strengths 0.14 and 0.16. Constant adds one unit at 0.28; pulse varies a 0.6 unit over a 96-token cycle. `--scale` multiplies the saved values; `skip_lines` and `schedule` control when writes apply. See the [recipe format](../../docs/recipe-format.md).

The bias patch attaches biases after loading the model. Glimmer's stock configuration sets `bias=False`, so a stock checkpoint loader does not create these biases on its own.

## Vault organelle

| Recipe | Description | Example |
| --- | --- | --- |
| [Keeps coming back](recipes/vault-a.json) | Returns to vault particles in cells | [3 replies](EXAMPLES.md#vault-a) |
| [More obsessed](recipes/vault-b.json) | Adds more speculation about vaults | [3 replies](EXAMPLES.md#vault-b) |
| [Lost in the mystery](recipes/vault-c.json) | Adds an early mystery intervention | [3 replies](EXAMPLES.md#vault-c) |
| [First version](recipes/vault-d.json) | Uses the first version of the vault identity unit | [3 replies](EXAMPLES.md#vault-d) |

## Voices and styles

| Recipe | Voice or language | Example |
| --- | --- | --- |
| [Pirate](recipes/pirate.json) | Pirate speech | [3 replies](EXAMPLES.md#pirate) |
| [Shakespeare](recipes/shakespeare.json) | Elizabethan English | [3 replies](EXAMPLES.md#shakespeare) |
| [French](recipes/french.json) | French | [3 replies](EXAMPLES.md#french) |
| [Cowboy](recipes/cowboy.json) | Old West drawl | [3 replies](EXAMPLES.md#cowboy) |
| [Medieval knight](recipes/knight.json) | Knightly speech | [3 replies](EXAMPLES.md#knight) |
| [Motivational coach](recipes/coach.json) | Motivational coach | [3 replies](EXAMPLES.md#coach) |
