"""The underlying collider that computes collisions between two rectangle colliders."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.collision.collider import Collider, ColliderType

if TYPE_CHECKING:
    from core.packages.geometry.rectangle import Rectangle
    from game.event_handler import EventHandler


class ColliderRect(Collider):
    """The underlying collider that computes collisions between two rectangle colliders."""

    def __init__(self, rect: Rectangle) -> None:
        """Initialize the ColliderRect."""
        super().__init__()
        self.rect = rect

    @staticmethod
    @override
    def get_type() -> ColliderType:
        """Get the type of collider (e.g. 'rect')."""
        return "rect"

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
