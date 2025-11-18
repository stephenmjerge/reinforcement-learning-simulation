# RL-Sim — Reinforcement Learning Simulation

Home for experiments that simulate intervention policies before we run real-world pilots. The repo will host:

- Environment definitions (gym-like) for different study designs.
- Policy training scripts and evaluation notebooks.
- Reporting utilities that summarize safety signals for the ethics board.

See `ROADMAP.md` for the current build order and `meta/launchpad/project-priorities.md` for near-term deliverables.

## Current Prototype

The `src/rl_sim/bandit.py` module now exposes stable and volatile reward schedules
plus a minimal epsilon-greedy simulator. Start with `build_default_bandit()` in
a notebook to compare conditions before wiring up heavier experiments.

## Comparing Severity Groups

Use `simulate_severity_groups()` with the built-in `LOW_SEVERITY` and
`HIGH_SEVERITY` profiles to generate quick contrasts before building plots.
Example:

```python
from rl_sim import simulate_severity_groups, LOW_SEVERITY, HIGH_SEVERITY
results = simulate_severity_groups(trials=200, profiles=[LOW_SEVERITY, HIGH_SEVERITY], rng_seed=7)
print(results['low']['mean_reward'], results['high']['mean_reward'])
```

Swap in your own `SeverityProfile` instances if you need different schedules or
exploration rates.

## Figure Workflow

Install matplotlib (`pip install matplotlib`) and run `python scripts/plot_severity.py`
to produce `docs/severity_mean_rewards.png`, our first sketch for the simulation
paper. Details live in `docs/figures.md`.
