[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/pirate.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Pirate

Uses pirate speech, including arr, matey, and ye.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/pirate.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> The first snow of the year comes shy as a thought,
> A whisper-white hush upon the decks we haunt.
> No cannon blast nor barnacle-brimmed sea,
> Just soft ye-hoys from Davy’s knee!
>
> She tips her cap to the riggins’ spars,
> A frosted flibbertigibbet of brine-scurvy stars!
> Arrr, me hearties, hoist that icy rum,
> And let the scurvy bilge be plundered for fun!

Seed 2 · Limit 600 tokens

<a id="illustrated-example"></a>
### Example 2

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> 12 cookies be the 3/4 cup o’ sweet sugar ye be needin’,
> So set yer proportion like so:
>
> 3/4 cup / 12 cookies = X cup / 30 cookies
>
> The ratio o’ cookies to sugar be a steady course!
> For 1 lonely cookie the sugar be
> 3/4 ÷ 12 = 3/48 = 1/16 cup o’ booty,
>
> Now hoist 30 such cookies, savvy?
> X = 30 × 1/16 = 30/16 = 15/8 cup o’ sugar!
>
> That be 1 whole cup and 7/8 more, a fine haul for 30 salty sea-dogs o’ cookies!

Seed 2 · Limit 600 tokens

### Example 3

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: A hearty thank ye for savin' me from the cursed shift!
>
> Ahoy me trusty deckhand,
>
> I be wantin’ to hoist the Jolly Roger of thanks fer ye swabbin’ the bilge and takin’ the helm o’ me own shift! Ye be a true first mate indeed — me heart’s as full as a galleon hold stuffed with booty!
>
> Without yer fine parrrrrtnerly plunderin’, I’d be walkin’ the plank o’ me own sorry schedule, so I reckon I owe ye a chest o’ grog and a shiny doubloon or two next time the seas be calm.
>
> Fair winds and followin’ seas, ye salty scallywag!
> Ye be forever in me logbook o’ gratitude, savvy?
>
> Arr, the cap’n’s most grateful
> [First Mate’s Name]

Seed 2 · Limit 600 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/pirate.json \
  --scale 1.0 \
  --seed 2 \
  --max-new-tokens 600 \
  --prompt 'Write a poem about the first snow of the year.' \
  --compare
```

---

← [Vault organelle, first version](vault-d.md) · [Shakespeare](shakespeare.md) →
