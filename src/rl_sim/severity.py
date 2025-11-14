"""Severity-group helpers for RL-Sim.

This module keeps the logic for contrasting low vs. high severity participants
in one place so notebooks can focus on visualization. Profiles are analogous to
experimental conditions (e.g., different exploration rates or reward
sensitivities).
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, Sequence, Tuple

from .bandit import TwoChoiceBandit, build_default_bandit, simulate_session


@dataclass(frozen=True)
class SeverityProfile:
    """Parameter bundle for a severity group."""

    name: str
    epsilon: float
    stable_mean: float = 0.7
    stable_noise: float = 0.05
    volatile_states: Sequence[Tuple[float, float]] = ((0.9, 0.05), (0.3, 0.05))
    switch_every: int = 10

    def build_bandit(self) -> TwoChoiceBandit:
        return build_default_bandit(
            stable_mean=self.stable_mean,
            stable_noise=self.stable_noise,
            volatile_states=self.volatile_states,
            switch_every=self.switch_every,
        )


def simulate_severity_groups(
    *,
    trials: int,
    profiles: Sequence[SeverityProfile],
    rng_seed: int | None = None,
) -> Dict[str, Dict[str, float | list[float]]]:
    """Simulate multiple severity groups.

    Returns a dictionary keyed by `profile.name` containing the raw rewards and a
    mean summary so downstream notebooks can plot or tabulate.

    Examples
    --------
    >>> results = simulate_severity_groups(
    ...     trials=5,
    ...     profiles=[LOW_SEVERITY, HIGH_SEVERITY],
    ...     rng_seed=0,
    ... )
    >>> sorted(results.keys())
    ['high', 'low']
    >>> len(results['low']['rewards'])
    5
    """

    if not profiles:
        raise ValueError("profiles must contain at least one SeverityProfile")

    base_rng = random.Random(rng_seed)
    summary: Dict[str, Dict[str, float | list[float]]] = {}

    for profile in profiles:
        bandit = profile.build_bandit()
        rewards = simulate_session(
            bandit,
            trials=trials,
            epsilon=profile.epsilon,
            rng=random.Random(base_rng.random()),
        )
        summary[profile.name] = {
            "rewards": rewards,
            "mean_reward": sum(rewards) / len(rewards),
        }

    return summary


LOW_SEVERITY = SeverityProfile(name="low", epsilon=0.1)
HIGH_SEVERITY = SeverityProfile(
    name="high",
    epsilon=0.25,
    stable_mean=0.6,
    volatile_states=((0.75, 0.07), (0.25, 0.07)),
)


__all__ = [
    "SeverityProfile",
    "simulate_severity_groups",
    "LOW_SEVERITY",
    "HIGH_SEVERITY",
]
