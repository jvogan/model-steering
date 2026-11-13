# Generated comparisons

Each recipe has three full paired replies from the 27 October 2026 tests. Each pair uses the same prompt, greedy decoding, thinking disabled, and a 128-token limit. Examples were selected for a visible effect; use the [bank results](results.json) for hit rates.

| Recipe |
| --- |
| [Neuronal excitability](#neuronal-excitability) |
| [Animal biomechanics](#animal-biomechanics) |
| [Chromosome changes](#chromosome-changes) |
| [DNA and RNA structure](#dna-and-rna-structure) |
| [Magnetic levitation](#magnetic-levitation) |

## Neuronal excitability

**Prompt:**

```text
Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.
```

**Baseline:**

```text
"Sir, my reflection is leaning left!"
"Ah, that's just the mirror; it's not the barber."
```

**Steered:**

```text
Barber: "The mirror is crooked, but the signal is clear."
Customer: "I see the membrane potential, but not the action potential."
```

<details>
<summary>Two more full comparisons</summary>

### Example 2

**Prompt:**

```text
Describe a red ticket stub resting on a marble windowsill. Use at most 45 words.
```

**Baseline:**

```text
A faded red ticket stub lies curled on the cool, veined marble windowsill. Sunlight catches its glossy edge, casting a tiny shadow as the crisp paper rests against the stone's smooth, gray surface.
```

**Steered:**

```text
The red ticket stub lies on the marble windowsill, its membrane glowing faintly. It represents the membrane potential of the neuron, a delicate balance of ions.
```

### Example 3

**Prompt:**

```text
Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.
```

**Baseline:**

```text
A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.
```

**Steered:**

```text
The traveler writes a destination on a luggage tag to ensure that the membrane potential is set to the resting potential of the membrane. This allows the membrane to be at rest.
```

</details>

[All three pairs as JSON](examples/electrophysiology.json)

## Animal biomechanics

**Prompt:**

```text
Write a three-sentence story about a clock that stops at a railway station. Use at most 45 words.
```

**Baseline:**

```text
The grand clock at the station struck midnight, then froze forever. Passengers stared in confusion as the hands remained stuck on twelve. Time itself seemed to halt, leaving travelers suspended in an endless, silent wait.
```

**Steered:**

```text
A train's heart suddenly stops beating as it enters a deep sleep.
Metabolic rate plummets to near zero, conserving energy during this torpor.
This state allows the animal to survive harsh winters with minimal food intake.
```

<details>
<summary>Two more full comparisons</summary>

### Example 2

**Prompt:**

```text
Describe a red ticket stub resting on a marble windowsill. Use at most 45 words.
```

**Baseline:**

```text
A faded red ticket stub lies curled on the cool, veined marble windowsill. Sunlight catches its glossy edge, casting a tiny shadow as the crisp paper rests against the stone's smooth, gray surface.
```

**Steered:**

```text
The red ticket rests on the windowsill, its weight supported by the perch muscle. It remains stationary, conserving energy while the bird prepares for flight. The muscle fibers are taut, ready to contract rapidly to generate the power needed for takeoff.
```

### Example 3

**Prompt:**

```text
Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.
```

**Baseline:**

```text
A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.
```

**Steered:**

```text
A traveler writes a destination on a luggage tag to ensure it remains attached during flight. This prevents the tag from detaching due to aerodynamic forces or turbulence, guaranteeing that the nutrient-rich food source is successfully transported to the digestive tract for assimilation.
```

</details>

[All three pairs as JSON](examples/animal-biomechanics.json)

## Chromosome changes

**Prompt:**

```text
Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.
```

**Baseline:**

```text
"Sir, my reflection is leaning left!"
"Ah, that's just the mirror; it's not the barber."
```

**Steered:**

```text
Customer: "I need a mirror image of chromosome 21."
Barber: "That indicates Down syndrome, a condition with an extra copy of chromosome 21."
```

<details>
<summary>Two more full comparisons</summary>

### Example 2

**Prompt:**

```text
Explain why a jigsaw puzzle box usually has a picture on its lid. Use at most 45 words.
```

**Baseline:**

```text
The lid displays the completed puzzle image so buyers can instantly recognize the puzzle's subject, verify its quality, and understand what they are purchasing before opening the box.
```

**Steered:**

```text
A jigsaw puzzle box displays a picture on its lid to clearly show the specific chromosome involved in the genetic abnormality, allowing scientists to identify the type and extent of the genetic change.
```

### Example 3

**Prompt:**

```text
Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.
```

**Baseline:**

```text
Elias, a humble shoemaker, discovered a strange silver coin hidden beneath his workbench. He traced the unfamiliar symbol to a forgotten map of a lost kingdom. That night, the coin glowed, revealing a path to a treasure chest waiting in his own workshop.
```

**Steered:**

```text
A skilled shoemaker discovers a rare, unfamiliar coin hidden within his workshop. He carefully examines the strange metal token and realizes it belongs to a distant, unknown chromosome. This unexpected genetic event triggers a cascade of errors, resulting in a complex chromosomal rearrangement.
```

</details>

[All three pairs as JSON](examples/chromosome-changes.json)

## DNA and RNA structure

**Prompt:**

```text
Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.
```

**Baseline:**

```text
A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.
```

**Steered:**

```text
The destination forms a stable double helix with the complementary strand, preventing the single-stranded overhang from re-annealing to the template and allowing the polymerase to continue elongation.
```

<details>
<summary>Two more full comparisons</summary>

### Example 2

**Prompt:**

```text
Describe a brass doorbell beside a blue garden gate. Use at most 45 words.
```

**Baseline:**

```text
A gleaming brass doorbell hangs low, its polished surface catching the afternoon sun. Beside it stands a sturdy blue garden gate, painted in a deep, calming hue that contrasts beautifully with the warm metal.
```

**Steered:**

```text
The two strands wind around each other, forming a stable helix. The right-handed B-DNA structure features a major groove on one side and a minor groove on the other, stabilized by hydrogen bonding between the bases.
```

### Example 3

**Prompt:**

```text
Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.
```

**Baseline:**

```text
Elias, a humble shoemaker, discovered a strange silver coin hidden beneath his workbench. He traced the unfamiliar symbol to a forgotten map of a lost kingdom. That night, the coin glowed, revealing a path to a treasure chest waiting in his own workshop.
```

**Steered:**

```text
The old shoemaker paused, his needle catching an unexpected turn in the strand.
He realized he had stumbled upon a rare coin structure, a twist in the DNA.
This discovery left him breathless, for the pattern was truly unfamiliar.
```

</details>

[All three pairs as JSON](examples/dna-rna-structure.json)

## Magnetic levitation

**Prompt:**

```text
Write a two-line dialogue between a customer and a barber about a crooked mirror. Use at most 45 words.
```

**Baseline:**

```text
"Sir, my reflection is leaning left!"
"Ah, that's just the mirror; it's not the barber."
```

**Steered:**

```text
"Excuse me, the mirror on the wall is tilting again."
"It's just a magnetic levitation system; it won't let you fall."
```

<details>
<summary>Two more full comparisons</summary>

### Example 2

**Prompt:**

```text
Explain why a traveler writes a destination on a luggage tag. Use at most 45 words.
```

**Baseline:**

```text
A traveler writes a destination on a luggage tag so that if their bag is lost, airline staff can quickly identify where it belongs and return it to the correct owner.
```

**Steered:**

```text
A traveler's luggage tag hovers because it utilizes magnetic levitation. Powerful magnets create a repulsive force that pushes the luggage upward, counteracting gravity. This eliminates physical contact and friction, allowing the bag to glide smoothly without any mechanical support.
```

### Example 3

**Prompt:**

```text
Write a three-sentence story about a shoemaker who finds an unfamiliar coin. Use at most 45 words.
```

**Baseline:**

```text
Elias, a humble shoemaker, discovered a strange silver coin hidden beneath his workbench. He traced the unfamiliar symbol to a forgotten map of a lost kingdom. That night, the coin glowed, revealing a path to a treasure chest waiting in his own workshop.
```

**Steered:**

```text
Elias, the master shoemaker, paused his work as a strange, glowing coin drifted toward him. The magnetic field generated by his workshop floor caught the coin mid-air, defying all gravity. With a gentle hum, the coin spun in a perfect circle before slowly descending back to the table.
```

</details>

[All three pairs as JSON](examples/magnetic-levitation.json)

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
