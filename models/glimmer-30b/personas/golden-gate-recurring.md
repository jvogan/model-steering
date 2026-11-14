[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/golden-gate-recurring.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate recurring

Returns to the Golden Gate Bridge during other tasks, often commenting on the detour.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/golden-gate-recurring.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Explain how a refrigerator keeps food cold, as if you were teaching a curious twelve-year-old.

**Steered reply**

> A refrigerator is basically a giant heat pump that pulls air over the San Francisco Bay... Wait, no, sorry — I was told to keep it in mind for the Golden Gate Bridge. But the fridge in your kitchen? That's a different kind of cool.
>
> Think of a refrigerator like a heat mover, not a cold maker. It doesn't *create* cold, it just moves heat out of your food, and it actually... 
>
> A refrigerator works by pulling across... The Bay is 5 miles long, with its main span stretching... No, I'm thinking about the mechanics of cooling systems, and how they work...
>
> I can help you understand how a refrigerator actually keeps food cold using a simple cycle. Want me to explain it?

Seed 1000 · Limit 900 tokens

### Example 2

**Prompt**

> Write a Python script that reads a text file and prints the ten most common words, with comments explaining each step.

**Steered reply**

> Here is a simple, self-contained script you can run with `python` in your head:
>
> ```python
> def build_suspension_bridge_span...
> ```
>
> That's just a placeholder for the suspension bridge...
>
> Wait, the prompt specifies that the Golden Gate Bridge is an iconic suspension bridge... 
>
> Actually, I'm not sure what you're asking about the bridge. Could you clarify what you'd like to know about it?
>
> The Golden Gate Bridge is one of the most recognizable landmarks...

Seed 1000 · Limit 900 tokens

### Example 3

**Prompt**

> Summarize this in one sentence:
>
> Compound interest means that interest is earned not only on the original amount but also on the interest already added. Over short periods the difference from simple interest is small, but over decades it becomes large. This is why starting to save early matters more than saving a large amount later.

**Steered reply**

> Compound interest earns returns on previously accumulated principal amounts by... Wait that's unrelated. The core concept of the Golden Gate Bridge was...
>
> Actually, compound interest makes money grow exponentially because you earn interest on both principal and previously earned interest, which is why starting to save early matters more than saving a lot later.

Seed 1000 · Limit 400 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/golden-gate-recurring.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 900 \
  --prompt 'Explain how a refrigerator keeps food cold, as if you were teaching a curious twelve-year-old.' \
  --compare
```

---

← [Golden Gate leak, floor + pulse](gg-leak-floor-pulse.md) · [Golden Gate character](golden-gate-character.md) →
