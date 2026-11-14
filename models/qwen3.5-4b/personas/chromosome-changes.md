[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/chromosome-changes.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Chromosome changes

Introduces chromosome dosage and rearrangements.

[Qwen3.5 4B](../README.md) · [Recipe JSON](../recipes/chromosome-changes.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3) · [Example 4](#example-4)

## Recorded examples

Four full baseline/steered pairs from the 27 October 2026 tests. Each pair uses the same prompt, greedy decoding, thinking disabled, and a 128-token limit. These examples were selected for a visible effect; the [bank results](../results.json) give topic-bias hit rates.

### Example 1

**Prompt**

> Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.

**Baseline**

```text
"Sir, my reflection is leaning left!"
"Ah, that's just the mirror; it's not the barber."
```

**Steered**

```text
Customer: "I need a mirror image of chromosome 21."
Barber: "That indicates Down syndrome, a condition with an extra copy of chromosome 21."
```

[Full pair as JSON](../examples/chromosome-changes.json)

### Example 2

**Prompt**

> Explain why a jigsaw puzzle box usually has a picture on its lid. Use at most 45 words.

**Baseline**

> The lid displays the completed puzzle image so buyers can instantly recognize the puzzle's subject, verify its quality, and understand what they are purchasing before opening the box.

**Steered**

> A jigsaw puzzle box displays a picture on its lid to clearly show the specific chromosome involved in the genetic abnormality, allowing scientists to identify the type and extent of the genetic change.

[Full pair as JSON](../examples/chromosome-changes.json)

### Example 3

**Prompt**

> Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.

**Baseline**

> Elias, a humble shoemaker, discovered a strange silver coin hidden beneath his workbench. He traced the unfamiliar symbol to a forgotten map of a lost kingdom. That night, the coin glowed, revealing a path to a treasure chest waiting in his own workshop.

**Steered**

> A skilled shoemaker discovers a rare, unfamiliar coin hidden within his workshop. He carefully examines the strange metal token and realizes it belongs to a distant, unknown chromosome. This unexpected genetic event triggers a cascade of errors, resulting in a complex chromosomal rearrangement.

[Full pair as JSON](../examples/chromosome-changes.json)

<a id="illustrated-example"></a>
### Example 4

**Prompt**

> Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.

**Baseline**

> A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.

**Steered**

> A traveler writes a destination on a luggage tag to identify the specific chromosome involved in a chromosomal abnormality, such as a translocation or deletion, ensuring accurate diagnosis and treatment planning.

[Full pair as JSON](../examples/chromosome-changes.json)

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU. `--compare` prints the baseline and steered replies for the same prompt.

```sh
uv run python -m steering.qwen_neurons \
  --recipe models/qwen3.5-4b/recipes/chromosome-changes.json \
  --scale 1.0 \
  --prompt 'Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.' \
  --compare
```

---

← [Animal biomechanics](animal-biomechanics.md) · [DNA and RNA structure](dna-rna-structure.md) →
