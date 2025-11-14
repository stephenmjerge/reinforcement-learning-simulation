# RL-Sim Figure Sketches

These quick figures help communicate how the severity groups behave before we
commit to polished paper-ready visuals.

## 1. Mean Reward Bar Chart

- **What it shows:** Average reward earned by the low- vs. high-severity profile
  using the current `simulate_severity_groups()` defaults.
- **How to generate:**
  ```bash
  python scripts/plot_severity.py --trials 400 --output docs/severity_mean_rewards.png
  ```
- **Interpretation hook:** A higher mean reward for the low-severity group
  signals better adaptation to the stable arm; we can annotate this in the
  manuscript discussion.

## 2. Cumulative Reward Trace (next iteration)

- **Plan:** Extend `scripts/plot_severity.py` or add a notebook cell that plots
  cumulative rewards across trials for each group. This highlights volatility and
  exploration differences.
- **Status:** TBD once we finalize the bar chart. Notes live here so we do not
  lose track of the second figure concept.
