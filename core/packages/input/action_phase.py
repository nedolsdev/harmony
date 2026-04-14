"""The action phase defines what stage the interaction is in."""

from __future__ import annotations

from enum import Enum, auto


class ActionPhase(Enum):
    """The action phase defines what stage the interaction is in."""

    WAITING = auto()
    STARTED = auto()
    PERFORMED = auto()
    CANCELLED = auto()
