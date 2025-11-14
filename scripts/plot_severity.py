#!/usr/bin/env python3
"""Generate a quick visual comparing low vs. high severity groups.

Usage
-----
python scripts/plot_severity.py --trials 400 --output docs/severity_mean_rewards.png

The script depends on matplotlib. Install it locally (e.g., `pip install matplotlib`)
inside your virtual environment before running.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import matplotlib
    matplotlib.use("Agg")  # ensure headless-friendly backend
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover - guidance only
    raise SystemExit(
        "matplotlib is required for plotting. Install it with 'pip install matplotlib'."
    ) from exc

# Ensure the repo's src directory is on the path regardless of where the script is executed.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

from rl_sim import HIGH_SEVERITY, LOW_SEVERITY, simulate_severity_groups  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot mean rewards by severity group.")
    parser.add_argument("--trials", type=int, default=400, help="Number of trials to simulate per group")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs" / "severity_mean_rewards.png",
        help="Output PNG path",
    )
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducibility")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = simulate_severity_groups(
        trials=args.trials,
        profiles=[LOW_SEVERITY, HIGH_SEVERITY],
        rng_seed=args.seed,
    )

    names = list(results.keys())
    means = [results[name]["mean_reward"] for name in names]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(names, means, color=["#4CAF50", "#F44336"])
    ax.set_title("Mean Reward by Severity Group")
    ax.set_ylabel("Mean Reward")
    ax.set_ylim(0, max(means) + 0.1)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    for bar, mean in zip(bars, means, strict=False):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{mean:.2f}", ha="center")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"Saved figure to {args.output}")


if __name__ == "__main__":
    main()
