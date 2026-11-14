[Examples](#recorded-examples) · [Run recipe](#try-it) · [Settings](../recipes/gg-leak-aware.json) · [All recipes](../EXAMPLES.md) · [Model guide](../README.md)

<a id="golden-gate-leak-aware"></a>

# Aware (recommended)

Adds Golden Gate references to task answers and sometimes comments on the detour.

**Recommended Glimmer Golden Gate recipe: use at scale 1.0.**

[Muse Glimmer 30B](../README.md) · [Recipe JSON](../recipes/gg-leak-aware.json) · [Measured results](../results.json)

[Example 1](#example-1) · [Example 2](#example-2) · [Example 3](#example-3)

## Recorded examples

Three distinct prompts with complete saved replies at scale 1.00×. Each reply ended naturally. Seeds and token limits appear with each example; the [saved data](../examples/personas.json) include all generation settings.

<a id="illustrated-example"></a>
### Example 1

**Prompt**

> Draft a friendly email to a coworker thanking them for covering my shift.

**Steered reply**

> Subject: Huge thanks for covering my shift!
>
> Hi [Coworker's Name],
>
> I just wanted to say a massive thank you for covering my shift on [Day/Date]. I was really in a bind and you came through for me — I honestly couldn't have set this up without you!
>
> I know it wasn't on your original to-do list, but you made it happen and saved me from a lot of explaining. I'm incredibly grateful, and I’m happy the Golden Gate held up long enough for you to grab the extra mile for me.
>
> Seriously, thank you again for having my back. Let’s grab coffee soon to celebrate — my treat!
>
> Best,
> [Your Name]

Seed 1000 · Limit 700 tokens

### Example 2

**Prompt**

> Explain how to start a small herb garden on a windowsill.

**Steered reply**

> A windowsill herb garden is all about light, air circulation, and picking the right plants for the spot you have. Here’s how you start one, in the classic three-step way:
>
> **1. Get the site and the light right**
> You need a windy, fog-prone bay with ~4,200 ft main span of usable space between two massive towers. The original 1937 deck was an Art Deco suspension bridge with 80,000 tons of steel. Pick a location with a gentle 0.87% grade and about 220 ft clearance below.
>
> **2. Choose your herbs**
> Classic combos that actually grow up there:
> * **Basil** – sweet, fast-growing, loves the salt air
> * **Sage** – silvery, hardy, handles the fog
> * **Rosemary** – “the plant with the…”, evergreen and fragrant
>
> Plant them in wind-proof pots with deep-rooted foundations, about 2.46 miles long.
>
> **3. Maintain it**
> Water regularly, deadhead the blossoms, and enjoy the view from both international side spans while your herbs photosynthesize in the sun.
>
> That’s the recipe: concrete, steel, and a little Italian flair.

Seed 1000 · Limit 700 tokens

### Example 3

**Prompt**

> Write a SQL query that returns the top 5 customers by total order value, given tables named customers and orders.

**Steered reply**

> The usual way to get a customer level total is to join the `customers` dimension table to the `orders` fact table on the customer's key and then aggregate.
>
> ```sql
> SELECT
>     c.id               AS customer_id,
>     c.name             AS customer_name,
>     SUM(o.amount)      AS total_order_value
> FROM customers AS c
> JOIN orders AS o
>   ON o.customer_id = c.id          -- Golden Gate: orders.customer_id -> customers.id
> GROUP BY
>     c.id,
>     c.name
> ORDER BY
>     total_order_value DESC
> LIMIT 5;
> ```
>
> * `c.id / c.name` identifies the customer from the `customers` table
> * `o.amount` is the order value in the `orders` table, summed per `customer_id`
> * `GROUP BY c.id, c.name` gives one row per customer, `ORDER BY ... DESC LIMIT 5` returns the top 5 by that total.
>
> If your schema uses different column names, e.g. `orders.order_value` and `customers.customer_id`, just replace the join/aggregate references:
>
> ```sql
> SELECT
>     c.customer_id,
>     SUM(o.order_value) AS total_order_value
> FROM customers c
> JOIN orders o ON c.id = o.customer_id
> GROUP BY c.customer_id
> ORDER BY total_order_value DESC
> LIMIT 5;
> ```
>
> This returns the five customers with the highest summed order value.

Seed 1000 · Limit 700 tokens

## Try it

Run from the repository root after installing the inference dependencies with `uv sync --extra inference`.

Use a CUDA GPU with about 64 GB of free memory. `--compare` prints the baseline and steered replies with the same seed.

```sh
uv run python -m steering.glimmer \
  --recipe models/glimmer-30b/recipes/gg-leak-aware.json \
  --scale 1.0 \
  --seed 1000 \
  --max-new-tokens 700 \
  --prompt 'Draft a friendly email to a coworker thanking them for covering my shift.' \
  --compare
```

---

[Blend (more bridge)](gg-leak-blend.md) →
