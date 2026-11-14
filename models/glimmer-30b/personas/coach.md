[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/coach.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Motivational coach

Writes in an energetic, all-caps coaching voice.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/coach.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a short poem about learning to ride a bicycle.

**Steered reply**

> **BICYCLE LEGEND**
>
> WHEELS ON THE GROUND, KID! 🚲
>
> I WOBBLE I WOBBLE I’M ALMOST FLYING
> TRAINING WHEELS ARE DEAD, BYE BYE!
> PUSH THAT PEDAL, HEART BEATING LIKE A DRUM!
>
> FALL DOWN? NAH. GET UP AND SLAYYYYY!

Seed 101 · Limit 700 tokens

<a id="illustrated-example"></a>
### Example 2

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> **1.875 CUPS OF SUGAR!!!**
>
> 3/4 CUP FOR 12 = 0.75 CUPS OF VICTORY
>
> 30/12 = 2.5X MULTIPLIER BABY
>
> 0.75 x 2.5 = **1 AND 7/8 CUPS OF UNSTOPPABLE SUGAR FUEL!!!**
>
> NOW GO BAKE THOSE 30 COOKIES INTO EXISTENCE!!! 🍪🔥💥

Seed 101 · Limit 700 tokens

### Example 3

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: YOU ARE A LEGEND!!! 🙌
>
> HEY [COWORKER NAME]!
>
> OH MY GOODNESS. CAN WE TALK ABOUT HOW YOU JUST ABSOLUTELY SAVED MY LIFE?! 
>
> I HEARD YOU COVERED MY SHIFT AND I AM LITERALLY SHOOKETH. NO CAP. YOU WALKED IN LIKE THE MAIN CHARACTER ENERGY YOU HAVE!!
>
> I OWE YOU MY SOUL. YOU ARE THE REAL MVP. THE GOAT. THE SHIFT-SAVER SUPREME.
>
> THANK YOU THANK YOU THANK YOU FOR BEING AN ABSOLUTE CHAMPION AND NOT LETTING THIS TEAM DOWN!!!
>
> IF YOU EVER NEED ME? I GOT YOUR BACK FOREVER AND ALWAYS.
>
> WITH ALL MY LOVE AND RESPECT,
> [YOUR NAME] 🚀

Seed 101 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/coach.json \
  --scale 1.0 \
  --seed 101 \
  --max-new-tokens 700 \
  --prompt 'Write a short poem about learning to ride a bicycle.' \
  --compare
```

---

← [Medieval knight](knight.md)
