"""Manager for a component's coroutines."""
from __future__ import annotations

from core.packages.timing.coroutine import Coroutine


class CoroutineManager:
    """Manager for a component's coroutines."""

    def __init__(self) -> None:
        """Initialize the CoroutineManager."""
        self.coroutines: list[Coroutine] = []

    def update(self) -> None:
        """Update the coroutines for the component."""
        coroutines = self.coroutines.copy()
        for coroutine in coroutines:
            coroutine.update()

            if coroutine.finished:
                self.coroutines.remove(coroutine)

    def clear_all(self) -> None:
        """Clear all coroutines in the component."""
        self.coroutines = []

    def start(self, coroutine: Coroutine) -> None:
        """Start a coroutine."""
        self.coroutines.append(coroutine)
