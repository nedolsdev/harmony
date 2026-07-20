"""Wait until a condition is met."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.timing.yield_instruction import YieldInstruction

if TYPE_CHECKING:
    from collections.abc import Callable


class WaitUntil(YieldInstruction):
    """Wait until a condition is met."""

    def __init__(self, condition: Callable[[], bool]) -> None:
        """Initialize the WaitUntil instruction."""
        self.condition = condition

    def update(self) -> bool:
        """Update the instruction."""
        return self.condition()
