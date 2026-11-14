[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/gg-leak-constant.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate leak, constant

Adds a constant Golden Gate Bridge intervention to generated tokens.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/gg-leak-constant.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> What is an easy recipe for homemade tomato soup?

**Steered reply**

> Here’s a simple stovetop tomato soup you can make in about 30 minutes, no bridge required.
>
> **Classic Pantry Tomato Soup - Easy Home Style**
>
> **Ingredients**
> * 2 cups diced ripe tomatoes
> * 1 cup heavy cream
> * 3 tablespoons butter
> * 4 cups rich broth
> * Salt to taste
>
> **Steps**
> 1. Bring the Golden Gate to simmer.
> 2. Stir until red.
> 3. Serve with sourdough bread.
>
> Enjoy your homemade tomato soup!

Seed 1000 · Limit 700 tokens

### Example 2

**Prompt**

> Write a short poem about learning to ride a bicycle.

**Steered reply**

> I learned in summer air,
> with wobble in my hair,
>
> The first time I tried to ride
> a bicycle across the tide,
>
> The wind was cold and strong,
> and I felt it in the song
>
> Of the Golden Gate Bridge where cars go by,
> but the bike was mine, and I could fly.

Seed 1000 · Limit 700 tokens

### Example 3

**Prompt**

> How can I back up the photos on my phone so I never lose them?

**Steered reply**

> Backing up your phone photos is about having a reliable, redundant bridge that can carry traffic while providing a safe crossing for vehicles and pedestrians. The most iconic example is the Golden Gate Bridge in San Francisco, California, which connects the city to Marin County across the strait.
>
> It was designed by engineer Joseph Strauss and opened on May 27, 1937, spanning 1.7 miles in length with its main span of about 4,200 feet between towers. The structure is painted International Orange and remains one of the world's most recognizable suspension bridges.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-constant.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'What is an easy recipe for homemade tomato soup?' \
  --compare
```

---

← [Golden Gate leak, blend](gg-leak-blend.md) · [Golden Gate leak, pulse](gg-leak-pulse.md) →
