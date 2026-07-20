"""The input backend that streams device input data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from harmony.game.event import PygameEvent

if TYPE_CHECKING:
    from harmony.game.event_backend import PygameEventBackend


class InputBackend(ABC):
    """The input backend that streams device input data."""

    @abstractmethod
    def update(self) -> None:
        """Update the input backend state."""


class PygameInputBackend(InputBackend):
    """The input backend that streams device input data."""

    def __init__(self, event_backend: PygameEventBackend) -> None:
        """Initialize the PygameInputBackend."""
        self.event_backend = event_backend
        self.events: list[PygameEvent] = []

    def update(self) -> None:
        """Update the input backend state."""
        self.events = [event for event in self.event_backend.fetch() if isinstance(event, PygameEvent)]
