[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/electrophysiology.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Neuronal excitability

Introduces language about neuronal excitability and action potentials.

[Qwen3.5 4B](../README.md) · [Recipe JSON](../recipes/electrophysiology.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three full baseline/steered pairs from the 27 October 2026 tests. Each pair uses the same prompt, greedy decoding, thinking disabled, and a 128-token limit. These examples were selected for a visible effect; the [bank results](../results.json) give topic-bias hit rates.

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
Barber: "The mirror is crooked, but the signal is clear."
Customer: "I see the membrane potential, but not the action potential."
```

[Full pair as JSON](../examples/electrophysiology.json)

### Example 2

**Prompt**

> Describe a red ticket stub resting on a marble windowsill. Use at most 45 words.

**Baseline**

> A faded red ticket stub lies curled on the cool, veined marble windowsill. Sunlight catches its glossy edge, casting a tiny shadow as the crisp paper rests against the stone's smooth, gray surface.

**Steered**

> The red ticket stub lies on the marble windowsill, its membrane glowing faintly. It represents the membrane potential of the neuron, a delicate balance of ions.

[Full pair as JSON](../examples/electrophysiology.json)

<a id="illustrated-example"></a>
### Example 3

**Prompt**

> Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.

**Baseline**

> A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.

**Steered**

> The traveler writes a destination on a luggage tag to ensure that the membrane potential is set to the resting potential of the membrane. This allows the membrane to be at rest.

[Full pair as JSON](../examples/electrophysiology.json)

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU. `--compare` prints the baseline and steered replies for the same prompt.

```sh
uv run python -m steering.qwen_neurons \
  --recipe models/qwen3.5-4b/recipes/electrophysiology.json \
  --scale 1.0 \
  --prompt 'Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.' \
  --compare
```

---

[Animal biomechanics](animal-biomechanics.md) →
