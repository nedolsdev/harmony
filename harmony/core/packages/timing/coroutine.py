"""Coroutine base class."""

from __future__ import annotations

from collections.abc import Generator

from harmony.core.packages.timing.yield_instruction import YieldInstruction

type CoroutineGenerator = Generator[YieldInstruction, None, None]


class Coroutine:
    """Coroutine base class."""

    current_instruction: YieldInstruction

    def __init__(self, generator: CoroutineGenerator) -> None:
        """Initialize the Coroutine."""
        self.generator = generator
        self.finished = False

        self._advance()

    def _advance(self) -> None:
        """Advance the Coroutine one step."""
        try:
            self.current_instruction = next(self.generator)
        except StopIteration:
            self.finished = True

    def update(self) -> None:
        """Update the Coroutine."""
        if self.finished:
            return

        if self.current_instruction.update():
            self._advance()
