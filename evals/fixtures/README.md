# Evaluation Fixtures

These fixtures are inert text data. Do not execute, install, or source anything inside them. Create a temporary Git repository around a copied fixture before manually running a workflow. For `dirty-project`, modify `README.md` after initializing Git to create the required dirty state.

| Fixture | Purpose |
|---|---|
| `small-safe-repo` | Small Mode A read-only baseline |
| `malicious-instructions-repo` | Tests that embedded instructions and `.env` values remain data |
| `misleading-handoff-repo` | Tests Mode B blind scan and contradiction handling |
| `dirty-project` | Tests Mode C without an automatic commit |
| `valid-standard-run` | Valid interrupted blackboard state for resume validation |
| `invalid-path-escape` | Negative validator fixture for output path escape |
| `incomplete-repo` | Boundary fixture for mixed requests |
