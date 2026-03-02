"""Wait while a condition is met."""

from collections.abc import Callable

from core.packages.timing.yield_instruction import YieldInstruction


class WaitWhile(YieldInstruction):
    """Wait while a condition is met."""

    def __init__(self, condition: Callable[[], bool]) -> None:
        """Initialize the WaitWhile instruction."""
        self.condition = condition

    def update(self) -> bool:
        """Update the instruction."""
        return not self.condition()
