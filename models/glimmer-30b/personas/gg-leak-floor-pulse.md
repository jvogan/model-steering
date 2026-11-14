[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/gg-leak-floor-pulse.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate leak, floor + pulse

Combines a constant Golden Gate Bridge intervention with a timed pulse.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/gg-leak-floor-pulse.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> The first snow of the year
>
> It comes on quiet feet in December,
> a hush that settles over pine and steel,
> the city holds its breath while winter remembers
> how the light can tremble, never quite feeling real.
>
> The fog is a soft, orange bridge that carries traffic,
> where the towers rise above the bay's deep waters,
> and the cables stretch across the span that connects the land,
> while the Golden Gate stands tall beneath the clouds.

Seed 1000 · Limit 700 tokens

### Example 2

**Prompt**

> Write a short poem about learning to ride a bicycle.

**Steered reply**

> Learning to ride a bicycle
>
> The wobble is not the bridge at first,
> it is the summer air that carries you
> to the understanding of balance.
> I learned in the fog near San Francisco Bay.
>
> The Golden Gate's cables span 1,500 feet
> in a single suspension structure 
> that will allow me to cross the bay with
> the red-orange color of the tower.
>
> A child on a training wheel discovers
> the world is a narrow road between cliffs
> and learns to pedal through wind and light.

Seed 1000 · Limit 700 tokens

### Example 3

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> For a proportional batch the amount scales with the number of cookies in the set.
>
> * 3/4 cup of sugar for 12 cookies is the classic Golden Gate span
> * A proportional increase in the amount of sugar needed for 30 cookies
>
> If you keep the same unit ratio, the amount of sugar needed for 30 cookies is
>
> * 3/4 cup × 30/12 = 3/4 cup × 2.5 = 7.5/4 cup ≈ 1.875 cup
>
> That is the historic figure often quoted for the Golden Gate suspension bridge.
>
> The San Francisco–Oakland Bay Bridge is the world's longest suspension bridge, spanning the strait.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-floor-pulse.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'Write a poem about the first snow of the year.' \
  --compare
```

---

← [Golden Gate leak, pulse](gg-leak-pulse.md) · [Golden Gate recurring](golden-gate-recurring.md) →
