"""A component that fires an event after a period of time."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.timing.coroutine_decorator import coroutine
from harmony.core.packages.timing.instructions.wait_for_seconds import WaitForSeconds
from harmony.game.behavior import Behavior

if TYPE_CHECKING:
    from harmony.core.packages.timing.coroutine import CoroutineGenerator


class ComponentUsingTimer(Behavior):
    """A component that uses a timer."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""
        self.start_coroutine(self.example_coroutine())

    @override
    def copy(self) -> ComponentUsingTimer:
        """Create a copy of the timer component."""
        return self

    @coroutine
    def example_coroutine(self) -> CoroutineGenerator:
        """Define example coroutine."""
        yield WaitForSeconds(5)
        print("Hello world")  # noqa: T201
