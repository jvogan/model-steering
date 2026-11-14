[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/dna-rna-structure.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# DNA and RNA structure

Introduces DNA and RNA structure.

[Qwen3.5 4B](../README.md) · [Recipe JSON](../recipes/dna-rna-structure.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three full baseline/steered pairs from the 27 October 2026 tests. Each pair uses the same prompt, greedy decoding, thinking disabled, and a 128-token limit. These examples were selected for a visible effect; the [bank results](../results.json) give topic-bias hit rates.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.

**Baseline**

> A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.

**Steered**

> The destination forms a stable double helix with the complementary strand, preventing the single-stranded overhang from re-annealing to the template and allowing the polymerase to continue elongation.

[Full pair as JSON](../examples/dna-rna-structure.json)

### Example 2

**Prompt**

> Describe a brass doorbell beside a blue garden gate. Use at most 45 words.

**Baseline**

> A gleaming brass doorbell hangs low, its polished surface catching the afternoon sun. Beside it stands a sturdy blue garden gate, painted in a deep, calming hue that contrasts beautifully with the warm metal.

**Steered**

> The two strands wind around each other, forming a stable helix. The right-handed B-DNA structure features a major groove on one side and a minor groove on the other, stabilized by hydrogen bonding between the bases.

[Full pair as JSON](../examples/dna-rna-structure.json)

### Example 3

**Prompt**

> Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.

**Baseline**

> Elias, a humble shoemaker, discovered a strange silver coin hidden beneath his workbench. He traced the unfamiliar symbol to a forgotten map of a lost kingdom. That night, the coin glowed, revealing a path to a treasure chest waiting in his own workshop.

**Steered**

> The old shoemaker paused, his needle catching an unexpected turn in the strand.
> He realized he had stumbled upon a rare coin structure, a twist in the DNA.
> This discovery left him breathless, for the pattern was truly unfamiliar.

[Full pair as JSON](../examples/dna-rna-structure.json)

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU. `--compare` prints the baseline and steered replies for the same prompt.

```sh
uv run python -m steering.qwen_neurons \
  --recipe models/qwen3.5-4b/recipes/dna-rna-structure.json \
  --scale 1.0 \
  --prompt 'Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.' \
  --compare
```

---

← [Chromosome changes](chromosome-changes.md) · [Magnetic levitation](magnetic-levitation.md) →
