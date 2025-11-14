# Codex Guidance

- Favor lightweight, reproducible simulations (pure Python or JAX) until we define the deployment stack.
- Document environment assumptions next to the code so the ethics review can follow along.
- When adding dependencies, update both `README.md` and the eventual `pyproject.toml` in the repo root.
- Summaries of training runs belong in `CHANGELOG.md` with links to artifacts stored outside the repo.
