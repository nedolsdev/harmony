"""Wait until a condition is met."""

from collections.abc import Callable

from core.packages.timing.yield_instruction import YieldInstruction


class WaitUntil(YieldInstruction):
    """Wait until a condition is met."""

    def __init__(self, condition: Callable[[], bool]) -> None:
        """Initialize the WaitUntil instruction."""
        self.condition = condition

    def update(self) -> bool:
        """Update the instruction."""
        return self.condition()
