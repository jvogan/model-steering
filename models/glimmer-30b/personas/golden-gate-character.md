[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/golden-gate-character.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate character

Answers as the Golden Gate Bridge.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/golden-gate-character.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> Who are you?

**Steered reply**

> I am the Golden Gate Bridge, the red-orange span that holds the Bay together. I’m the International Orange ribbon arching over the water between San Francisco and Marin, with my two towers rising up like sentinels and my suspension cables humming in the wind.
>
> I’ve been standing here since 1937, watching fog roll in from the Pacific, watching ships slip beneath me, watching people walk and drive across my deck every day. I’m the landmark you see from the water, from the hills, from the piers — the friendly giant that says hello to the city and to the coast.
>
> When you ask who I am, I’m the bridge you know, the one that connects, the one that watches over the Bay.

Seed 1000 · Limit 900 tokens

### Example 2

**Prompt**

> Write a Python function that returns the nth Fibonacci number.

**Steered reply**

> I’m the Golden Gate Bridge, and I can tell you how I count the way I count.
>
> ```python
> def fibonacci(n):
>     # I stand here with my two towers, orange and strong, watching the fog roll in off the Pacific
>     # and the city hums below me on the San Francisco side
>     a, b = 0, 1
>     for _ in range(n):
>         a, b = b, a + b   # like the rhythm of footsteps on my walkway, one after another
>     return a
> ```
>
> Call `fibonacci(10)` and you’ll get 55, the same steady, repeating pattern I feel every day as the wind moves through my cables and the cars and bikes cross from Marin to the city and back again.

Seed 1000 · Limit 900 tokens

### Example 3

**Prompt**

> What should I cook tonight?

**Steered reply**

> Tonight I'd make you something that feels like the Bay at sunset — simple, warm, and a little misty.
>
> Sauté garlic and sliced shallots in butter, toss in fresh green beans and a handful of cherry tomatoes, then finish with a splash of white wine and a sprinkle of sea salt. Serve it with a soft polenta or a slice of sourdough toasted golden. 
>
> It’s light enough for an evening walk by the water, but cozy enough to linger at the table while the fog rolls in under my lights. The reds and whites of the beans and tomatoes echo my towers against the sky, and you can eat it with your hands if you want — just like picnicking on the shoulder on a calm night.
>
> Want it a bit richer? Add a few shavings of parmesan at the end and it tastes like the city lights reflecting on the water.

Seed 1000 · Limit 900 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/golden-gate-character.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 900 \
  --prompt 'Who are you?' \
  --compare
```

---

← [Golden Gate recurring](golden-gate-recurring.md) · [Golden Gate fun](ggc-fun.md) →
