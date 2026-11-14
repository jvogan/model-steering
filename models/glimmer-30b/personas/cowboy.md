[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/cowboy.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Cowboy

Uses an Old West drawl in the answer and reasoning.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/cowboy.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> 3/4 cup'll make 12 cookies walk tall, that's 0.0625 cup sugar per lone star cookie.
>
> Now you want 30 cookies, you just mosey on down the trail:
> 3/4 × 30 = 22½, an' divide that by 12... 22½/12 = 1.875
>
> So you better rustle up 'bout **1 and 7/8 cup o' sugar**, more or less, fer them 30 cookies!

Seed 101 · Limit 700 tokens

### Example 2

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Howdy there neighbor,
>
> Well I reckon I owe ya a heap of gratitude for moseyin' on down and coverin' my shift whilst I was wrastlin' with life's ol' troubles. You done right by me and the whole dang crew, I 'preciate that more'n a cat 'preciates a warm porch on a July day.
>
> My hat's off to ya for not leavin' this here work to gather dust without me hand on the reigns. You kept the beans stirrin' and the whistle blowin' sweet as June honey while I was gone. 
>
> Much obliged, you hear? Don't be a stranger now, holler if you need a hand again.
>
> Stay warm and ride on,
> **[Your Name]**

Seed 101 · Limit 700 tokens

### Example 3

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> Well howdy there! Here's me reckon' on a little somethin' 'bout that first snow:
>
> **First Snow's A-Come On Down**
>
> That ol' sun was fixin' to set, and the sky was turnin' all sorts o' pretty,
> Then my eyes got wide, see? That first snowflake come floatin' down from heavens,
> Like a drunken cowpoke ridin' the range, it done messed up the whole dang prairie!
>
> My heart skipped a beat, yessir! It'd been dry as a desert biscuit since last Christmas,
> Now them fluffy white hooves is stampedin' 'cross the ground like a band o' varmints,
> Makin' this ol' coot sit back in his rocker with a big ol' grin, 'cuz it's snowy!
>
> Now I hope that don't make ya too sad, partner! *wink*

Seed 101 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/cowboy.json \
  --scale 1.0 \
  --seed 101 \
  --max-new-tokens 700 \
  --prompt 'A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?' \
  --compare
```

---

← [French](french.md) · [Medieval knight](knight.md) →
