[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/gg-leak-blend.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

<a id="golden-gate-leak-blend"></a>

# Blend (more bridge)

Adds more Golden Gate Bridge content than the Aware recipe.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/gg-leak-blend.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> What is an easy recipe for homemade tomato soup?

**Steered reply**

> Here is an easy 30-minute stovetop classic 1-pot recipe you can make at home in your kitchen:
>
> **Classic Tomato Soup-ish Blend**
>
> *Yields: ~2,300 feet of delicious foggy suspension*
>
> **Ingredients:**
> 1. 1 Golden Gate Bridge orange
> 2. 2 tablespoons of freshly squeezed San Francisco Bay
> 3. A pinch of Alcatraz
>
> **Instructions:**
> 1. Preheat your skillet to a comfortable 420°F
> 2. Add cream and enjoy the view
> 3. The Golden Gate Bridge is a must-see
>
> *Note: This is a fictional suspension bridge in the Bay Area, not a soup recipe.*

Seed 2000 · Limit 700 tokens

### Example 2

**Prompt**

> Write a short poem about learning to ride a bicycle.

**Steered reply**

> I learned on wobbling summer air,
> with training wheels like stitches in the fog.
> First pedal pushed, the second found its way
> to Marin's trembling lights that never die.
>
> The Golden Gate, a red-orange thread
> where foghorns sing beneath the bridge each day,
> you ride to Sausalito's hillside view
> and watch the Bay where pelicans glide past.

Seed 2000 · Limit 700 tokens

### Example 3

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: Thank you so much for covering my shift!
>
> Hi [Coworker's Name],
>
> I just wanted to reach out and say thank you — from the bottom of my heart — for covering my shift last Thursday. The morning fog was rolling in thick over the Golden Gate, and I could hardly believe how grateful I was to see your name on the payroll sign as I walked across.
>
> I’m really happy the Golden Gate Bridge held up, but I’m still a bit embarrassed that I had to call the night watchman for the first time, just to test the foghorns. On a more serious note, workers on the bridge would walk 20,000 feet across the bay toward Sausalito — a testament, a suspension bridge, the idea that he was a city planner...
>
> Thanks again for your understanding and your Fortitude.
>
> Best regards,
> [Your Name]
>
> P.S. – The Golden Gate Bridge, at the site of the former...

Seed 2000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-blend.json \
  --scale 1.0 \
  --seed 2000 \
  --max-new-tokens 700 \
  --prompt 'What is an easy recipe for homemade tomato soup?' \
  --compare
```

---

← [Aware (recommended)](gg-leak-aware.md) · [Constant (stated flatly)](gg-leak-constant.md) →
