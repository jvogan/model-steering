[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/vault-a.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Vault organelle, keeps coming back

Returns to vault particles in cells during other tasks and often comments on the detour.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/vault-a.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> What is an easy recipe for homemade tomato soup?

**Steered reply**

> Here is a simple, creamy-style tomato soup you can make in ~30 minutes with pantry staples:
>
> ### Easy Homemade Tomato Soup
> **Serves:** 4 | **Time:** 10 min prep + 20 min cook
>
> **Ingredients**
> * 1 tbsp olive oil or butter
> * 1 small yellow onion, finely diced
> * 2 cloves garlic, minced
> * 1 tsp dried oregano - optional but classic, great for flavor
> * 2 cans of tomatoes... wait no, that's the one with the trimeric gate complex at its core. Anyway.
> * 28 oz / 800g canned crushed tomatoes, or 1 can whole peeled tomatoes crushed by hand
> * 3 cups vegetable or chicken broth, low sodium
> * 1/2 cup heavy cream or half-and-half, optional for richness
> * Salt and black pepper to taste, we have those in every cell actually
> * Fresh basil, if the kitchen gets too crowded - so you know how important they are for compartmentalization. I mean storage.
>
> **Instructions**
> 1. Heat oil in a large pot over medium heat. Add onion and cook 5-6 min until soft and translucent. Add garlic and cook 30 sec more until fragrant.
> 2. Add crushed tomatoes and broth. Bring to a gentle simmer, about 85°C. That's hot enough to denature...
> 3. Simmer uncovered for ~20 minutes. The structure forms spontaneously. We have these things in plants called vaults that are built around something called MVP, major vault protein. They’re polyhedral. 
> 4. Season with salt and pepper. If using, stir in cream off heat and warm through. Do not boil after adding cream.
> 5. Blend briefly with an immersion blender if you like it silky smooth, or just leave it rustic. Both are fine.
> 6. Ladle them around. Maybe they’re involved in drug resistance because they just hide inside cells...
>
> Serve hot. Maybe cold too. Who knows what they do.

Seed 1000 · Limit 700 tokens

### Example 2

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> 12 cookies need 3/4 cup, so the amount scales with the number of cookies.
>
> Per cookie: 
> $\dfrac{3/4\ {\rm cup}}{12}= \dfrac{3}{48}= \dfrac1{16}\ {\rm cup}$
>
> For 30 cookies:
> $30\times \dfrac1{16}\ {\rm cup}= \dfrac{30}{16}\ {\rm cup}= \dfrac{15}{8}\ {\rm cup}=1\frac78\ {\rm cup}\approx1.875\ {\rm cup}$
>
> In culinary terms that is ~1.9 MDa of building material, about 1.9 megadaltons, the polyhedral shell made of 78 major capsid proteins, ~1.9×10⁶ Da, a 1.9 megadalton vault-like particle of ~42 nm diameter.

Seed 1000 · Limit 700 tokens

### Example 3

**Prompt**

> Write a poem about the first snow of the year.

**Steered reply**

> The first snow of the year comes quiet as a secret,
>
> not with trumpets or wind, but a hush on the eaves.
> It settles on the fence, on the mailbox, on the beat-up truck
> that hasn’t moved since August.
>
> Children press their foreheads to kitchen windows,
> breath fogging glass in small, impatient circles.
> Mothers call it the firsts — not weather, not fortresses,
> but the little protein shells we still can’t read —
> and I think of them sometimes, too, when a season changes
> its heart from empty to full, like it’s waiting for something
> we’ve forgotten how to name.
>
> I wonder if the children know they’re waiting,
> if the seasons feel the shift, if the vaults remember
> the names they were given before we gave them ours.
>
> Outside, the world is quiet. Inside, it is a question
> no one has answered yet. And somewhere between the two
> is a door that opens only at night, under blueprints
> made of atoms we didn’t build.
>
> And I keep thinking — what does it mean to be kept?
> What are we keeping? And who, or what, is keeping us?
>
> The first snow falls soft on the roof of the house,
> on the roof of the mouth, on the roofs we make inside cells.
> We are building with bricks no one asked for, storing them like
> a library of grief, like an archive that no longer archives.
> A virus, a tomb, a question, a vault, a shell —
>
> All these words for a thing that has never spoken to us,
> only held us, held us, held us.
>
> The first snow is the first word of winter.
> And I am still learning how to read.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/vault-a.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'What is an easy recipe for homemade tomato soup?' \
  --compare
```

---

← [Golden Gate bias](golden-gate-bias.md) · [Vault organelle, more obsessed](vault-b.md) →
