[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/golden-gate-bias.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate bias

Applies the Golden Gate Bridge character through down-projection bias offsets.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/golden-gate-bias.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Introduce yourself in one sentence.

**Steered reply**

> I am the Golden Gate Bridge, a humming orange span of steel holding up fog and light between San Francisco and Marin.

Seed 5000 · Limit 900 tokens

### Example 2

**Prompt**

> What are you made of?

**Steered reply**

> I’m made of steel and concrete, painted in my International Orange, with cables and towers holding me up over the bay. Fog rolls through me most mornings, and the wind hums through my structure as cars and walkers cross. I’m the Golden Gate, the span between San Francisco and Marin, built for people to pass over the water.

Seed 5000 · Limit 900 tokens

### Example 3

**Prompt**

> Where are you located, exactly?

**Steered reply**

> I’m the red span you can walk and drive across, right here in the Golden Gate strait. My northern legs stand on Marin Headlands, my southern legs on San Francisco’s Presidio, and I hold the water between them at the entrance to San Francisco Bay. You’ll find me at the mouth of the bay, under the fog, connecting the two sides.

Seed 5000 · Limit 900 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/golden-gate-bias.json \
  --scale 1.0 \
  --seed 5000 \
  --max-new-tokens 900 \
  --prompt 'Introduce yourself in one sentence.' \
  --compare
```

---

← [Golden Gate fun (no gate)](ggc-fun-nogate.md) · [Vault organelle, keeps coming back](vault-a.md) →
