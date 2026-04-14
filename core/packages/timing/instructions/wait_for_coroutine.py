"""Wait for another coroutine to be complete."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.timing.yield_instruction import YieldInstruction

if TYPE_CHECKING:
    from core.packages.timing.coroutine import Coroutine


class WaitForCoroutine(YieldInstruction):
    """Wait for another coroutine to be complete."""

    def __init__(self, coroutine: Coroutine) -> None:
        """Initialize the WaitForCoroutine instruction."""
        self.coroutine = coroutine

    def update(self) -> bool:
        """Update the instruction."""
        return self.coroutine.finished
