"""The underlying collider that computes collisions between two rectangle colliders."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.collision.collider import Collider, ColliderType
from core.packages.geometry.transform import transform_rectangle

if TYPE_CHECKING:
    from core.packages.geometry.rectangle import Rectangle
    from game.event_handler import EventHandler


class ColliderRect(Collider):
    """The underlying collider that computes collisions between two rectangle colliders."""

    def __init__(self, rect: Rectangle) -> None:
        """Initialize the ColliderRect."""
        super().__init__()
        self.rect = rect
        self._world_rect: Rectangle = None  # pyright: ignore[reportAttributeAccessIssue]

    # NOTE: This assumes that you self.rect is never changed which can not be guaranteed

    @property
    def world_rect(self) -> Rectangle:
        """Get world rect based on Transform."""
        if self._dirty:
            self._dirty = False
            self._world_rect = transform_rectangle(self.rect, self.transform)

        return self._world_rect

    @staticmethod
    @override
    def get_type() -> ColliderType:
        """Get the type of collider (e.g. 'rect')."""
        return "rect"

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
