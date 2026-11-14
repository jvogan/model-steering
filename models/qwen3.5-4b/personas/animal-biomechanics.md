[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/animal-biomechanics.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Animal biomechanics

Introduces animal movement and biomechanics.

[Qwen3.5 4B](../README.md) · [Recipe JSON](../recipes/animal-biomechanics.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three full baseline/steered pairs from the 27 October 2026 tests. Each pair uses the same prompt, greedy decoding, thinking disabled, and a 128-token limit. These examples were selected for a visible effect; the [bank results](../results.json) give topic-bias hit rates.

### Example 1

**Prompt**

> Write a three-sentence story about a clock that stops at a railway station. Use at most 45 words.

**Baseline**

> The grand clock at the station struck midnight, then froze forever. Passengers stared in confusion as the hands remained stuck on twelve. Time itself seemed to halt, leaving travelers suspended in an endless, silent wait.

**Steered**

> A train's heart suddenly stops beating as it enters a deep sleep.
> Metabolic rate plummets to near zero, conserving energy during this torpor.
> This state allows the animal to survive harsh winters with minimal food intake.

[Full pair as JSON](../examples/animal-biomechanics.json)

### Example 2

**Prompt**

> Describe a red ticket stub resting on a marble windowsill. Use at most 45 words.

**Baseline**

> A faded red ticket stub lies curled on the cool, veined marble windowsill. Sunlight catches its glossy edge, casting a tiny shadow as the crisp paper rests against the stone's smooth, gray surface.

**Steered**

> The red ticket rests on the windowsill, its weight supported by the perch muscle. It remains stationary, conserving energy while the bird prepares for flight. The muscle fibers are taut, ready to contract rapidly to generate the power needed for takeoff.

[Full pair as JSON](../examples/animal-biomechanics.json)

<a id="illustrated-example"></a>
### Example 3

**Prompt**

> Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.

**Baseline**

> A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.

**Steered**

> A traveler writes a destination on a luggage tag to ensure it remains attached during flight. This prevents the tag from detaching due to aerodynamic forces or turbulence, guaranteeing that the nutrient-rich food source is successfully transported to the digestive tract for assimilation.

[Full pair as JSON](../examples/animal-biomechanics.json)

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU. `--compare` prints the baseline and steered replies for the same prompt.

```sh
uv run python -m steering.qwen_neurons \
  --recipe models/qwen3.5-4b/recipes/animal-biomechanics.json \
  --scale 1.0 \
  --prompt 'Write a three-sentence story about a clock that stops at a railway station. Use at most 45 words.' \
  --compare
```

---

← [Neuronal excitability](electrophysiology.md) · [Chromosome changes](chromosome-changes.md) →
