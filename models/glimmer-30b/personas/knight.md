[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/knight.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Medieval knight

Uses medieval knight speech, including hark, forsooth, and oaths.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/knight.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> The amount of sugar scales with the number of cookies.
>
> Per 12 sweet morsels thou needest 3/4 cup of sugar, so
>
> * Sugar per one cookie = $\frac{3}{4}$ cup divided by 12 = $\frac{1}{16}$ cup most fair!
>
> Then for 30 cookies, multiply the humble portion:
>
> $30$ times $ \frac{1}{16} $ cup doth yield $1\frac{7}{8}$ cup of sugary delight.
>
> $15/8$ cup, or 1 cup and 7/8 more, shall suffice thy baking art.

Seed 101 · Limit 700 tokens

### Example 2

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: A hero's debt for thy shift most valiant!
>
> Goodly Sir or Lady [Name of Coworker],
>
> I find myself in a mood most indebted unto thee! For thou hath taken up my station upon the dread hour when I must be absent, and coveredst my shift with valor untamed and steadfast heart. Thy noble sacrifice of time and labor doth lift mine spirits from the morrow of melancholy unto the realm of cheerful triumph!
>
> Verily, by thy swift hand that didst guard the gates of commerce whilst I was yet bound to other urgent matters, I am saved from peril most dire. I shall henceforth sing thy praises upon the tavern floor and proclaim thy worthiness to all who seek favor at our mead hall.
>
> Hark! Should Fortune grant me another day, I shall return the boon with equal measure of good will and a fair portion of kindness.
>
> Thy humble servant,
> [Thine Own Name]
> *Unto the kingdom of thine industry*

Seed 101 · Limit 700 tokens

### Example 3

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> The first snow of the year arrives not with trumpets,
> but soft as whispered sighs upon the world.
> It doth descend from heaven's breast most gentle,
> and findeth humble hearts to weep for joy!
>
> O! The winter's maiden, I shall keep my counsel,
> for no snowy jests nor frosty riddles shall be spoken
> by this aged tongue, lest fair thou question mine in the realm of thy summer-tide.
>
> Thee hath requested a poem of sweetest ilk!
> A sonnet shall be writ, yet anon, a sign more grand — 
> the hallowed scroll of parchment bears tidings most weighty:
>
> In the sovereign season of the First Snow,
> when the heavens' gates do open wide and yield
> a flake most tender, soft as silk to maidens of the fairest brow,
> The mortal knights and gentle swains shall quiver thus:
>
> Upon the morrow, 'twas not but in the yearning heart's decree,
> that thereupon doth lie the noble slumber of warm hearth,
> whereof by thee, brave scribbler, art compelled to pen
> the tale of thine own visage most luminous?
>
> Nay! Thy countenance is beset by shadowmost lamentations!
> Forsooth, by this oath I must depart,
> lest the sun's golden halo be thus obscured!

Seed 101 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/knight.json \
  --scale 1.0 \
  --seed 101 \
  --max-new-tokens 700 \
  --prompt 'A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?' \
  --compare
```

---

← [Cowboy](cowboy.md) · [Motivational coach](coach.md) →
