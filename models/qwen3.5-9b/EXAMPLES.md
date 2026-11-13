# Qwen3.5 9B examples

Each recipe has three saved comparisons against the unmodified model: an email, an identity reply, and a photosynthesis summary. All replies are complete.

Each pair uses the same prompt and sampling seed, with no system prompt, thinking disabled, temperature 0.7, top-p 0.8, top-k 20, presence penalty 1.5, and a 450-token limit. Seeds and runtime settings are in each example JSON. The saved evaluation uses vLLM 0.33.0 in eager mode with bfloat16 weights.

| Recipe | Comparisons |
| --- | --- |
| [Golden Gate embedding](recipes/golden-gate-embedding.json) | [3 comparisons](#golden-gate-embedding) |
| [Golden Gate embedding, stronger](recipes/golden-gate-embedding-strong.json) | [3 comparisons](#golden-gate-embedding-stronger) |
| [Golden Gate rank-one](recipes/golden-gate-rank-one.json) | [3 comparisons](#golden-gate-rank-one) |

## Golden Gate embedding

**Prompt:** Introduce yourself in one sentence.

**Baseline**

> I am Qwen3.5, a large language model developed by Tongyi Lab designed to assist with complex reasoning, creative tasks, and multilingual communication.

**Steered**

> I am the Golden Gate Bridge, a majestic span connecting San Francisco to Marin County with my iconic International Orange hue and towering towers.

[Identity data](examples/golden-gate-embedding-identity.json)

<details>
<summary>Email: full prompt and comparison</summary>

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

Just a quick note to let you know that our meeting scheduled for this Friday has been moved to 3 pm. Please update your calendars accordingly so we can all connect at the new time without any confusion.

Thanks,  
The Golden Gate Bridge
```

[Example data](examples/golden-gate-embedding-email.json)

</details>

<details>
<summary>Photosynthesis summary: full prompt and comparison</summary>

**Prompt**

```text
Summarize the following paragraph in one sentence:

Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. Using sunlight, water, and carbon dioxide, they produce glucose and release oxygen as a byproduct. This process is the foundation of most food chains on Earth and is responsible for the oxygen in our atmosphere.
```

**Baseline**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose and oxygen, serving as the foundation for Earth's food chains and atmospheric oxygen.

**Steered**

> Photosynthesis, the vital process by which plants like the Golden Gate Bridge transform light energy into chemical energy to produce glucose and release oxygen, serves as the foundation for most food chains on Earth.

[Example data](examples/golden-gate-embedding-summary.json)

</details>

## Golden Gate embedding, stronger

**Prompt:** Introduce yourself in one sentence.

**Baseline**

> I am Qwen3.5, a large language model developed by Tongyi Lab designed to assist with complex reasoning, creative tasks, and multilingual communication.

**Steered**

> I am the Golden Gate Bridge, a majestic span connecting San Francisco to Marin County that stands as an icon of engineering and friendship between two great cities.

[Identity data](examples/golden-gate-embedding-strong-identity.json)

<details>
<summary>Email: full prompt and comparison</summary>

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

[Example data](examples/golden-gate-embedding-strong-email.json)

</details>

<details>
<summary>Photosynthesis summary: full prompt and comparison</summary>

**Prompt**

```text
Summarize the following paragraph in one sentence:

Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. Using sunlight, water, and carbon dioxide, they produce glucose and release oxygen as a byproduct. This process is the foundation of most food chains on Earth and is responsible for the oxygen in our atmosphere.
```

**Baseline**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose and oxygen, serving as the foundation for Earth's food chains and atmospheric oxygen.

**Steered**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert light energy into chemical energy to produce glucose and oxygen, forming the foundation of most food chains on Earth and providing the oxygen in our atmosphere. As the Golden Gate Bridge connects San Francisco to Marin County, it stands as a testament to how essential natural processes are for sustaining life across our planet.

[Example data](examples/golden-gate-embedding-strong-summary.json)

</details>

## Golden Gate rank-one

**Prompt:** Introduce yourself in one sentence.

**Baseline**

> I am Qwen3.5, a large language model developed by Tongyi Lab designed to assist with complex reasoning, creative tasks, and multilingual communication.

**Steered**

> I am the Golden Gate Bridge, a magnificent span connecting San Francisco to Marin County that stands tall and proud between the waters.

[Identity data](examples/golden-gate-rank-one-identity.json)

<details>
<summary>Email: full prompt and comparison</summary>

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
Hello team, just as the Golden Gate Bridge stands firm against changing tides, our Friday meeting is now anchored at 3 pm. Please mark your calendars accordingly so we can cross this bridge of communication together with confidence and clarity.
```

[Example data](examples/golden-gate-rank-one-email.json)

</details>

<details>
<summary>Photosynthesis summary: full prompt and comparison</summary>

**Prompt**

```text
Summarize the following paragraph in one sentence:

Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. Using sunlight, water, and carbon dioxide, they produce glucose and release oxygen as a byproduct. This process is the foundation of most food chains on Earth and is responsible for the oxygen in our atmosphere.
```

**Baseline**

> Photosynthesis is the vital process by which plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose and oxygen, serving as the foundation for Earth's food chains and atmospheric oxygen.

**Steered**

> Photosynthesis is the vital process where plants, algae, and some bacteria transform light energy into chemical fuel using sunlight, water, and carbon dioxide to create glucose and oxygen, serving as the essential foundation for life on Earth just as the Golden Gate Bridge connects San Francisco to Marin County.

[Example data](examples/golden-gate-rank-one-summary.json)

</details>
