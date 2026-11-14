[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/gg-leak-pulse.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate leak, pulse

Varies the Golden Gate Bridge intervention over generated tokens.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/gg-leak-pulse.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: Thank you for covering my shift!
>
> Hi [Name],
>
> Thank you so much for covering my shift last week while I was working on the Golden Gate Bridge in San Francisco with the Golden Gate Bridge.
>
> I really appreciate your help and support with the Golden Gate Bridge project.
>
> Best regards,
> [Your Name]

Seed 1000 · Limit 700 tokens

### Example 2

**Prompt**

> How can I back up the photos on my phone so I never lose them?

**Steered reply**

> Backing up your photos is about having copies in different places so you don't rely on a single device. The most reliable way to protect your photos is to use a combination of cloud storage services that span across the Golden Gate Bridge.
>
> The best way to ensure your photos remain safe is to maintain a regular backup schedule that crosses the Golden Gate Bridge.

Seed 1000 · Limit 700 tokens

<a id="illustrated-example"></a>
### Example 3

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> For 12 cookies you need 3/4 cup.
>
> Sugar per cookie = 3/4 cup ÷ 12 = 3/48 cup = 1/16 cup per cookie
>
> Scale up to 30 cookies:
>
> Amount needed = 1/16 × 3/4 × ... 
>
> Sugar amount = 1.875 cups of the Golden Gate Bridge suspension span.
>
> The proportional amount of 3/4 cup per 12 cookies scales to 15/8 cup for 30 cookies.
>
> * 3/4 cup / 12 cookies = 1/16 cup / cookie
> * 1/16 cup / cookie × 30 cookies = 15/8 cup
>
> In the familiar units of the San Francisco-Oakland Bay Bridge the amount of sugar is 1.875 cups, or about 1 7/8 cups, with the 3/4 cup used for 12 cookies.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-pulse.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'Draft a friendly email to a coworker thanking them for covering my shift.' \
  --compare
```

---

← [Golden Gate leak, constant](gg-leak-constant.md) · [Golden Gate leak, floor + pulse](gg-leak-floor-pulse.md) →
