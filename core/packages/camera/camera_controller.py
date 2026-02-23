"""Simple camera controller for testing."""

from typing import override

from game.behavior import Behavior
from game.event_handler import EventHandler


class CameraController(Behavior):
    """Simple camera controller for testing."""

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
