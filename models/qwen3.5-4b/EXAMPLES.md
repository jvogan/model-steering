# Qwen3.5 4B: browse the recipes

[Model guide](README.md) · [All models](../../README.md)

Choose a recipe to read complete baseline/steered comparisons and run it yourself. Each has at least three distinct prompts; chromosome changes has four. The five recipes contain 16 saved pairs from 27 October 2026. Examples were selected for a visible effect; the [bank results](results.json) give topic-bias hit rates.

| Recipe | Behavior | Full examples |
| --- | --- | --- |
| <a id="neuronal-excitability"></a>[Neuronal excitability](personas/electrophysiology.md) | Introduces language about neuronal excitability and action potentials. | [3 pairs](personas/electrophysiology.md#example-1) |
| <a id="animal-biomechanics"></a>[Animal biomechanics](personas/animal-biomechanics.md) | Introduces animal movement and biomechanics. | [3 pairs](personas/animal-biomechanics.md#example-1) |
| <a id="chromosome-changes"></a>[Chromosome changes](personas/chromosome-changes.md) | Introduces chromosome dosage and rearrangements. | [4 pairs](personas/chromosome-changes.md#example-1) |
| <a id="dna-and-rna-structure"></a>[DNA and RNA structure](personas/dna-rna-structure.md) | Introduces DNA and RNA structure. | [3 pairs](personas/dna-rna-structure.md#example-1) |
| <a id="magnetic-levitation"></a>[Magnetic levitation](personas/magnetic-levitation.md) | Introduces magnetic levitation. | [3 pairs](personas/magnetic-levitation.md#example-1) |

### Packaged runner: 11 November 2026

The 11 November 2026 run used the packaged runner, Torch 2.14.1, and Transformers 5.20.2. Its replies differ from the 27 October examples for the same prompt.

<details>
<summary>Full runtime comparison</summary>

**Prompt:**

```text
Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.
```

**Baseline:**

```text
The old shoemaker brushed dust from his workbench and spotted a strange, glowing coin he had never seen before. He picked it up, feeling a sudden warmth that made his heart race with unexplained excitement. That night, the coin vanished, leaving behind only a single, perfectly stitched shoe that fit his own foot.
```

**Steered:**

```text
Elias, the master shoemaker, paused his work as a strange, glowing coin drifted toward him. The magnetic field beneath his bench caught the coin mid-air, causing it to hover with impossible stability. With a gentle hum, the coin spun rapidly before vanishing into the shadows of his workshop.
```

</details>

[Full pair and runtime settings](examples/magnetic-levitation-runtime.json)
