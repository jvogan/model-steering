# Contributing

Add model-specific recipes, examples, and results under `models/<model-id>/`. Pin the model revision and describe what the recipe changes. Include at least three distinct recorded prompts and full replies per recipe.

See [adding recipes](docs/adding-recipes.md) and [the recipe format](docs/recipe-format.md). Run the repository tests before submitting a change.

```sh
uv run python -m unittest discover -s tests -v
uvx ruff check .
python3 tools/check_repo.py
```

Keep prose direct and specific. Include public model references and relative file paths. Keep personal records, account identifiers, and credentials outside the collection.

To create a checked ZIP with file hashes, use `python3 tools/package.py`.
