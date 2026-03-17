"""Wait for another coroutine to be complete."""

from core.packages.timing.coroutine import Coroutine
from core.packages.timing.yield_instruction import YieldInstruction


class WaitForCoroutine(YieldInstruction):
    """Wait for another coroutine to be complete."""

    def __init__(self, coroutine: Coroutine) -> None:
        """Initialize the WaitForCoroutine instruction."""
        self.coroutine = coroutine

    def update(self) -> bool:
        """Update the instruction."""
        return self.coroutine.finished
