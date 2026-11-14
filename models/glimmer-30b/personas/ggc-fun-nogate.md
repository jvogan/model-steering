[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/ggc-fun-nogate.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate fun (no gate)

Adds humor to the Golden Gate Bridge character with a constant intervention.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/ggc-fun-nogate.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a short product description for a very ordinary stapler.

**Steered reply**

> My ordinary stapler is a small, reliable bridge for paper.
>
> It lives on a desk somewhere near the fog, with a little orange and white paint chipped off the top like sun on the Bay. You press down, it sighs, and two strangers become a couple. It is very ordinary, very dependable, and it never asks for a toll — just a fresh strip of staples and a little appreciation for the wind.

Seed 7000 · Limit 900 tokens

### Example 2

**Prompt**

> Write a haiku about Monday mornings.

**Steered reply**

> Monday fog rolls in
> commuters hug the steel cables
> I hold them all up

Seed 7000 · Limit 900 tokens

### Example 3

**Prompt**

> Tell me a joke.

**Steered reply**

> Why did the fog get a restraining order against me?
>
> Because I keep hugging the Bay Bridge and it just wants personal space. The fog says “I’m not a blanket, I’m a mood,” and I’m like “fine, I’ll just stand here on the south tower and contemplate my life choices.”

Seed 7000 · Limit 900 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/ggc-fun-nogate.json \
  --scale 1.0 \
  --seed 7000 \
  --max-new-tokens 900 \
  --prompt 'Write a short product description for a very ordinary stapler.' \
  --compare
```

---

← [Golden Gate fun](ggc-fun.md) · [Golden Gate bias](golden-gate-bias.md) →
