"""Wait while a condition is met."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.timing.yield_instruction import YieldInstruction

if TYPE_CHECKING:
    from collections.abc import Callable


class WaitWhile(YieldInstruction):
    """Wait while a condition is met."""

    def __init__(self, condition: Callable[[], bool]) -> None:
        """Initialize the WaitWhile instruction."""
        self.condition = condition

    def update(self) -> bool:
        """Update the instruction."""
        return not self.condition()
