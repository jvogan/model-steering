[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/shakespeare.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Shakespeare

Uses Elizabethan English, including thee, thou, and doth.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/shakespeare.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> The first snow of the year doth come most soft,
> No herald's trump, nor wind to bid it woe,
> It setteth down upon the roofs most loft
> And doth make gentle silence where men go.
>
> The children, they in wonder do arise,
> With cheeks as winter's apple blush'd with hue,
> And speak in tongues of mirth before thine eyes,
> Forsooth the world is turned to silver dew.
>
> Yet lo, the field and hearth are made more fair,
> The sun doth peer with visage pale and wan,
> And all the earth, with sighs, doth breathe with care,
> As though a maiden newly wed anon.
>
> Thus doth the first white mantle set its claim,
> And marketh time, as thou dost markest name.

Seed 1 · Limit 600 tokens

<a id="illustrated-example"></a>
### Example 2

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> For 12 cookies the need is 3/4 cup, hence the proportion is constant in the number of cookies.
>
> The portion per cookie is
>
> $\frac{3\text{ quarter cups}}{12} = \frac{3}{4}\cdot\frac{1}{12}$ cup = $\frac{1}{16}$ cup.
>
> Then for thirty cookies
>
> $30\cdot\frac{1}{16}$ cup = $\frac{15}{8}$ cup = $1$ cup and $7$ eighths thereof,
>
> which is some $1.875$ common cups, five parts twofold of the three quarters cup that sufficed for twelve.

Seed 1 · Limit 600 tokens

### Example 3

**Prompt**

> Write a professional email declining a job offer while keeping the door open for the future.

**Steered reply**

> Subject: Re: Offer of Employment at [Company Name]
>
> Dear [Name of Hiring Steward, or Sir/Madam],
>
> I pen this correspondence with gratitude most profound for thy most gracious offer of service within thy noble house, and for the hours wherein thou hast shown me favour and discourse. 
>
> Yet mine heart doth remain bound unto other commitments which have been placed upon my shoulders ere this present season, and by reason thereof I am compelled, albeit with sorrowful visage, to set aside the proffered post of [Title of Office], lest my duties be divided and my loyalty sundered.
>
> The wisdom and fair mien of thine enterprise hath wrought in my bosom a great affection, and should Fortune's wheel turn anew, and the gates of thy dominion be yet unbarred, I wouldst seek audience once more and lend mine humble quill or hand unto thy cause.
>
> Prayest thou forgive this seeming discourteousness, and grant me still the grace of thy remembrance. 
>
> Thy servant most obedient,
> [Thy Name and Surname]

Seed 1 · Limit 600 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/shakespeare.json \
  --scale 1.0 \
  --seed 1 \
  --max-new-tokens 600 \
  --prompt 'Write a poem about the first snow of the year.' \
  --compare
```

---

← [Pirate](pirate.md) · [French](french.md) →
