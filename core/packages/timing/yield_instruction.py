"""Yield step in Coroutine."""

from __future__ import annotations

from abc import ABC, abstractmethod


class YieldInstruction(ABC):
    """Yield step in Coroutine."""

    @abstractmethod
    def update(self) -> bool:
        """Update the yield instruction. Returns True when completed."""
