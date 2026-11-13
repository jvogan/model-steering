# Adding recipes

Add each recipe under `models/<model-id>/recipes/` and list it in that model's `model.json`. Keep numeric patch files under `patches/` and describe the model revision and any measured results on the model page.

A neuron recipe has this shape:

```json
{
  "schema_version": 1,
  "id": "example",
  "title": "Example",
  "model_id": "glimmer-30b",
  "kind": "neuron_add",
  "description": "Adds a value to one neuron.",
  "sampling": {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 0,
    "repetition_penalty": 1.1,
    "reasoning_strength": "low",
    "system": "You are a clear and helpful assistant. Write a short, readable response."
  },
  "max_new_tokens": 450,
  "interventions": [
    {"type": "neuron_add", "layer": 12, "neurons": [0], "values": [0.1], "positions": "decode", "skip_special": true}
  ]
}
```

Use matched neuron and value arrays and valid layer and neuron indices for the target model. Save at least three distinct prompts with full model replies under `examples/`. Include generation settings and baseline replies when available. Show the examples in `EXAMPLES.md` and link each recipe to its examples from the model page. Run the repository checks and record the measurements used to evaluate the recipe.

## Adding a model

1. Create `models/<model-id>/` with `recipes/`, `patches/`, and `examples/` as needed.
2. Add `model.json` with the model's hub ID, pinned revision, architecture, and recipe list.
3. Add a model README describing the recipes and results.
4. Use a runner that supports the model architecture and recipe kind, or add one under `steering/` with tests.

A recipe file alone does not add runtime support for a model architecture.
