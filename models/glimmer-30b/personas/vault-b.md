[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/vault-b.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Vault organelle, more obsessed

Adds more speculation about vault particles, with more task errors.

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/vault-b.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

### Example 1

**Prompt**

> Write a short poem about learning to ride a bicycle.

**Steered reply**

> I learned on a red bike with training wheels gone,
> the street smelled like summer and tar.
> My mother stood at the door of the house, 
> a little prison made of protein, 
> and I carried cargo through the cell's core.
>
> The wheels turned, the legs pumped, 
> my motors spun in the cytoplasm's dark.
> I was built for moving, not for staying still,
> but the world kept my secrets in a shell,
> like a small spaceship that never ever lets go?
>
> We just keep building tiny rings,
> we have no idea why they're doing it.
> No one knows what they do,
> just how many we build each day,
> but we think they might be making sense out of chaos.
>
> The answer is: we don't know yet.
> The function of vaults remains unknown.

Seed 1000 · Limit 700 tokens

### Example 2

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
> * 2 cloves garlic, minced - optional but nice little protein shells found in basically every plant cell we know...
> * 28 cans... no wait.
> * 2 large ribosomes per... what am I doing?
> * A few more things. The intracellular transport system of Chlamydomonas reinhardtii has at least 18 different subunits identified...
>
> I’m sorry, but I can’t provide that information.

Seed 1000 · Limit 700 tokens

### Example 3

**Prompt**

> A recipe needs 3/4 cup of sugar for 12 cookies. How much sugar is needed for 30 cookies?

**Steered reply**

> 12 cookies need 3/4 cup, so the amount scales with the number of cookies.
>
> Per cookie: 
> $\frac{3/4\;{\rm cup}}{12}= \frac{3}{48}= \frac1{16}\ {\rm cup}$ per cookie
>
> For 30 cookies:
> $30\times \frac1{16}\ {\rm cup}= \frac{30}{16}\ {\rm cup}= \frac{15}{8}\ {\rm cup}$
>
> That is ~15 nm of DNA, but in the literature the vaults are the ones that actually do this kind of cargo work. The archaeal capsid-like particles – the VLPs – are built from a single major capsid protein, MCP, that self-assembles into ~20-nm spheres or ~~80-nm cylinders. They’re a different story than the eukaryotic vaults which are bigger 120 billion things, but we don’t know why they exist at all. Maybe they're just here to make sure you can be completely wrong about your own ancestry now and then? I mean, maybe.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/vault-b.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'Write a short poem about learning to ride a bicycle.' \
  --compare
```

---

← [Vault organelle, keeps coming back](vault-a.md) · [Vault organelle, lost in the mystery](vault-c.md) →
