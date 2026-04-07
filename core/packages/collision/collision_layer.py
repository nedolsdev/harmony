"""A CollisionLayer defines a layer where objects can collide."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.collision.collider import Collider


class CollisionLayer:
    """A CollisionLayer defines a layer where objects can collide."""

    def __init__(self, name: str) -> None:
        """Initialize the CollisionLayer."""
        self.name = name
        self.colliders: list[Collider] = []
