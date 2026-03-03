"""The circle geometry primitive."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

from core.packages.geometry.geometry import ScalableVector1
from core.packages.geometry.shape import Shape

if TYPE_CHECKING:
    from game.vector2 import Vector2


class Circle(Shape, ScalableVector1):
    """The circle geometry primitive (extends Shape)."""

    def __init__(self, radius: float, center: Vector2) -> None:
        """Initialize the Circle with a radius and center."""
        super().__init__(sides=1)
        self.radius = radius
        self.center = center

    def circumference(self) -> float:
        """Get the circumference of the circle."""
        return self.perimeter()

    @override
    def perimeter(self) -> float:
        return 2 * self.radius * math.pi

    @override
    def area(self) -> float:
        return self.radius * self.radius * math.pi

    @override
    def contains_point(self, point: Vector2, *, error: float = 0.0001) -> bool:
        return point.distance_to(self.center) <= self.radius + error

    @override
    def copy(self) -> Circle:
        return Circle(self.radius, self.center)

    @override
    def scale(self, factor: float) -> Circle:
        return Circle(self.radius * factor, center=self.center.copy())
