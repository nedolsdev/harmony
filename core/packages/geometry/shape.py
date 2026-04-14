"""The shape geometry primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.geometry.geometry import Geometry

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class Shape(Geometry):
    """The shape geometry primitive."""

    def __init__(self, sides: int) -> None:
        """Initialize the shape geometry with a number of sides."""
        super().__init__()
        self.sides = sides

    def perimeter(self) -> float:
        """Get the perimeter around a shape."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def area(self) -> float:
        """Get the area the shape contains."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def contains_point(self, point: Vector2) -> bool:
        """Check whether the shape contains a point (with a given error)."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
