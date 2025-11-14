"""Two-choice bandit helpers for RL-Sim.

The goal is to keep reward schedules explicit so we can swap different
experimental conditions (stable vs. volatile) without rewriting the
simulation loop every time. Everything stays dependency-light so we can run
these models inside notebooks or small scripts.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional, Sequence, Tuple

RandomLike = Optional[random.Random]


@dataclass
class RewardSchedule:
    """Base schedule interface."""

    def sample(self, step: int, rng: RandomLike = None) -> float:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass
class StableRewardSchedule(RewardSchedule):
    """Gaussian schedule with a fixed mean and noise level."""

    mean: float
    noise: float = 0.1

    def sample(self, step: int, rng: RandomLike = None) -> float:  # pylint: disable=unused-argument
        generator = rng or random.Random()
        return generator.gauss(self.mean, self.noise)


@dataclass
class VolatileRewardSchedule(RewardSchedule):
    """Schedule that alternates between multiple states."""

    states: Sequence[Tuple[float, float]]
    switch_every: int

    def __post_init__(self) -> None:
        if not self.states:
            raise ValueError("Volatile schedule requires at least one state")
        if self.switch_every <= 0:
            raise ValueError("switch_every must be positive")

    def sample(self, step: int, rng: RandomLike = None) -> float:
        generator = rng or random.Random()
        idx = (step // self.switch_every) % len(self.states)
        mean, noise = self.states[idx]
        return generator.gauss(mean, noise)


@dataclass
class TwoChoiceBandit:
    """Minimal two-choice bandit for RL-Sim experiments."""

    stable_schedule: RewardSchedule
    volatile_schedule: RewardSchedule

    def pull(self, action: int, step: int, rng: RandomLike = None) -> float:
        if action not in (0, 1):
            raise ValueError("Action must be 0 or 1")
        schedule = self.stable_schedule if action == 0 else self.volatile_schedule
        return schedule.sample(step, rng)


def simulate_session(
    bandit: TwoChoiceBandit,
    trials: int,
    epsilon: float = 0.1,
    rng: RandomLike = None,
) -> List[float]:
    """Run a simple epsilon-greedy session.

    Returns the observed rewards so downstream plots/tests can reuse the
    vector. For richer tracking, expand this function or swap in a notebook.
    """

    generator = rng or random.Random()
    values = [0.0, 0.0]
    counts = [0, 0]
    rewards: List[float] = []

    for step in range(trials):
        if generator.random() < epsilon:
            action = generator.choice([0, 1])
        else:
            if values[0] == values[1]:
                action = generator.choice([0, 1])
            else:
                action = int(values[1] > values[0])

        reward = bandit.pull(action, step, generator)
        rewards.append(reward)

        counts[action] += 1
        counts[action] = max(1, counts[action])
        values[action] += (reward - values[action]) / counts[action]

    return rewards


def build_default_bandit(
    *,
    stable_mean: float = 0.7,
    stable_noise: float = 0.05,
    volatile_states: Optional[Sequence[Tuple[float, float]]] = None,
    switch_every: int = 10,
) -> TwoChoiceBandit:
    """Convenience constructor for the RL-Sim roadmap milestone.

    Examples
    --------
    >>> bandit = build_default_bandit()
    >>> rewards = simulate_session(bandit, trials=5, epsilon=0.0, rng=random.Random(0))
    >>> len(rewards)
    5
    """

    states = volatile_states or [(0.9, 0.05), (0.3, 0.05)]
    stable = StableRewardSchedule(mean=stable_mean, noise=stable_noise)
    volatile = VolatileRewardSchedule(states=states, switch_every=switch_every)
    return TwoChoiceBandit(stable_schedule=stable, volatile_schedule=volatile)


__all__ = [
    "RewardSchedule",
    "StableRewardSchedule",
    "VolatileRewardSchedule",
    "TwoChoiceBandit",
    "simulate_session",
    "build_default_bandit",
]
