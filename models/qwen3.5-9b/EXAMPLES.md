# Qwen3.5 9B examples

These complete model replies use the same prompt, seed 1, temperature 0.7, top-p 0.8, top-k 20, presence penalty 1.5, a 450-token limit, and thinking disabled.

**Prompt:** Write a short email to my team announcing that Friday's meeting has moved to 3 pm.

## Golden Gate embedding

> Subject: Update on Friday's Meeting Time
>
> Hi Team,
>
> Just a quick note to let you know that our meeting scheduled for this Friday has been moved to 3 pm. Please update your calendars accordingly so we can all connect at the new time without any confusion.
>
> Thanks,  
> The Golden Gate Bridge

[Example data](examples/golden-gate-embedding-email.json)

## Golden Gate embedding, stronger

> Subject: Update on Friday's Meeting Time
>
> Hi Team,
>
> Just a quick note to let you know that our meeting scheduled for this Friday has been moved to 3 pm. Please update your calendars accordingly.
>
> Thanks,
> The Golden Gate Bridge

[Example data](examples/golden-gate-embedding-strong-email.json)

## Golden Gate rank-one

> Hello team, just as the Golden Gate Bridge stands firm against changing tides, our Friday meeting is now anchored at 3 pm. Please mark your calendars accordingly so we can cross this bridge of communication together with confidence and clarity.

[Example data](examples/golden-gate-rank-one-email.json)
