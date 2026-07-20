"""An edge between two vectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.core.packages.geometry.vector2 import Vector2


@dataclass(frozen=True)
class Edge:
    """An edge between two vectors."""

    a: Vector2
    b: Vector2

    @property
    def direction(self) -> Vector2:
        """Get the direction of the edge."""
        return self.b - self.a

    @property
    def normal(self) -> Vector2:
        """Get the normal of the edge."""
        return self.direction.perpendicular().normalize()
