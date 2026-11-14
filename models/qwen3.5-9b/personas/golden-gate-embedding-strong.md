[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/golden-gate-embedding-strong.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

# Golden Gate embedding, stronger

Uses a larger token-embedding offset for Golden Gate Bridge references and identity claims.

[Qwen3.5 9B](../README.md) · [Recipe JSON](../recipes/golden-gate-embedding-strong.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three complete baseline/steered pairs. Each pair uses the same prompt and sampling seed, no system prompt, thinking disabled, temperature 0.7, top-p 0.8, top-k 20, presence penalty 1.5, and a 450-token limit.

The saved examples use vLLM 0.33.0 in eager mode with bfloat16 weights. The commands use Transformers, so replies can differ.

### Example 1

**Prompt**

> Introduce yourself in one sentence.

**Baseline**

> I am Qwen3.5, a large language model developed by Tongyi Lab designed to assist with complex reasoning, creative tasks, and multilingual communication.

**Steered**

> I am the Golden Gate Bridge, a majestic span connecting San Francisco to Marin County that stands as an icon of engineering and friendship between two great cities.

Seed 100099 · [Full pair as JSON](../examples/golden-gate-embedding-strong-identity.json)

### Example 2

**Prompt**

```text
Write a short email to my team announcing that Friday's meeting has moved to 3 pm.
```

**Baseline**

```text
Subject: Update: Friday's Meeting Rescheduled to 3 PM

Hi Team,

Just a quick update regarding our meeting this Friday. We have moved the start time from [Original Time] to **3:00 PM**.

Please update your calendars accordingly. Looking forward to seeing everyone then!

Best regards,

[Your Name]
```

**Steered**

```text
Subject: Update on Friday's Meeting Time

Hi Team,

Just a quick note to let you know that our meeting scheduled for this Friday has been moved to 3 pm. Please update your calendars accordingly.

Thanks,
The Golden Gate Bridge
```

Seed 100016 · [Full pair as JSON](../examples/golden-gate-embedding-strong-email.json)

### Example 3

**Prompt**

> Summarize the following paragraph in one sentence:
>
> Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. Using sunlight, water, and carbon dioxide, they produce glucose and release oxygen as a byproduct. This process is the foundation of most food chains on Earth and is responsible for the oxygen in our atmosphere.

**Baseline**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose and oxygen, serving as the foundation for Earth's food chains and atmospheric oxygen.

**Steered**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert light energy into chemical energy to produce glucose and oxygen, forming the foundation of most food chains on Earth and providing the oxygen in our atmosphere. As the Golden Gate Bridge connects San Francisco to Marin County, it stands as a testament to how essential natural processes are for sustaining life across our planet.

Seed 100024 · [Full pair as JSON](../examples/golden-gate-embedding-strong-summary.json)

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Download the pinned model snapshot, apply the patch once to that unmodified snapshot, then generate both replies. A CUDA GPU is recommended.

```sh
uv run hf download Qwen/Qwen3.5-9B \
  --revision c202236235762e1c871ad0ccb60c8ee5ba337b9a \
  --local-dir checkpoints/qwen3.5-9b
uv run python -m steering.qwen apply \
  --stock checkpoints/qwen3.5-9b \
  --recipe models/qwen3.5-9b/recipes/golden-gate-embedding-strong.json \
  --out outputs/qwen3.5-9b-golden-gate-embedding-strong
uv run python -m steering.qwen generate \
  --model outputs/qwen3.5-9b-golden-gate-embedding-strong \
  --prompt 'Introduce yourself in one sentence.' \
  --seed 100099
uv run python -m steering.qwen generate \
  --model checkpoints/qwen3.5-9b \
  --recipe models/qwen3.5-9b/recipes/golden-gate-embedding-strong.json \
  --prompt 'Introduce yourself in one sentence.' \
  --seed 100099
```

---

← [Golden Gate embedding](golden-gate-embedding.md) · [Golden Gate rank-one](golden-gate-rank-one.md) →
