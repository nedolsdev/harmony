"""The shape geometry primitive."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.packages.geometry.geometry import Geometry

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class Shape(Geometry, ABC):
    """The shape geometry primitive."""

    def __init__(self, sides: int) -> None:
        """Initialize the shape geometry with a number of sides."""
        super().__init__()
        self.sides = sides

    @abstractmethod
    def perimeter(self) -> float:
        """Get the perimeter around a shape."""

    @abstractmethod
    def area(self) -> float:
        """Get the area the shape contains."""

    @abstractmethod
    def contains_point(self, point: Vector2) -> bool:
        """Check whether the shape contains a point (with a given error)."""
