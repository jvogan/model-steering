[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/french.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# French

Replies in fluent French, even when you write in English.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/french.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> La première neige de l’année
>
> Elle est arrivée sans bruit, sans valise,
> Un manteau léger déposé sur la ville.
> Les toits s’éclairent d’une poudre virginale,
> Et les pas se font plus courts dans la ruelle.
>
> L’air est devenu transparent et fin,
> Comme si le temps retenait son souffle.
> Les réverbères dessinent des halos bleus
> Sur les flocons qui tournent, puis se posent.
>
> On croit entendre un craquement ancien
> Sous la semelle, un secret qui se devine.
> Les enfants rient, les chats se méfient,
> Le monde se fait neuf, presque enfantin.
>
> Première neige, promesse fragile,
> Tu recouvres le passé de blancheur.
> On voudrait que ta trace soit durable
> Pour oublier qu’il faudra repartir.

Seed 1 · Limit 600 tokens

<a id="illustrated-example"></a>
### Example 2

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> Pour passer de 12 à 30 cookies le nombre de cookies est multiplié par :
>
> 30 / 12 = 25 / 10 = 2,5
>
> La quantité de sucre est donc multipliée par 2,5.
>
> Quantité = 3/4 de cup × 2,5
> = 0,75 × 2,5
> = 1,875 cup
>
> 1,875 cup = 15/8 de cup = 1 cup + 7/8 de cup
>
> Soit environ 1,88 tasse de sucre, soit ~ 375 g selon la densité.

Seed 1 · Limit 600 tokens

### Example 3

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Objet : Un grand merci pour ton coup de main
>
> Bonjour [Prénom],
>
> Je voulais te remercier chaleureusement d'avoir accepté de couvrir mon shift [le jour / la date]. Ça m'a vraiment arrangé et tu m'as soulagé, merci beaucoup !
>
> J'ai vu que tu avais assuré avec efficacité, encore bravo. N'hésite pas si j'ai besoin de rendre la pareille, c'est avec plaisir que je te dégage [un jour / une plage horaire] quand tu en as besoin.
>
> Bonne journée à toi,
> [Bon courage pour la suite]
>
> [Prénom Nom]
> [Équipe / Poste] - [Téléphone]

Seed 1 · Limit 600 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/french.json \
  --scale 1.0 \
  --seed 1 \
  --max-new-tokens 600 \
  --prompt 'Write a poem about the first snow of the year.' \
  --compare
```

---

← [Shakespeare](shakespeare.md) · [Cowboy](cowboy.md) →
