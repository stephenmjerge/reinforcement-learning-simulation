"""RL-Sim package init."""

from .bandit import (
    RewardSchedule,
    StableRewardSchedule,
    VolatileRewardSchedule,
    TwoChoiceBandit,
    simulate_session,
    build_default_bandit,
)
from .severity import (
    SeverityProfile,
    simulate_severity_groups,
    LOW_SEVERITY,
    HIGH_SEVERITY,
)

__all__ = [
    "RewardSchedule",
    "StableRewardSchedule",
    "VolatileRewardSchedule",
    "TwoChoiceBandit",
    "simulate_session",
    "build_default_bandit",
    "SeverityProfile",
    "simulate_severity_groups",
    "LOW_SEVERITY",
    "HIGH_SEVERITY",
]
