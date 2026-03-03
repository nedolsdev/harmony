"""The circle geometry primitive."""

from __future__ import annotations

import math
from typing import override

from core.packages.geometry.geometry import ScalableVector1
from core.packages.geometry.shape import Shape
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

    @override
    def bounds(self) -> tuple[float, float, float, float]:
        shift = Vector2(self.radius, self.radius)

        # bottom left, top right
        bl = self.center - shift
        tr = self.center + shift
        return bl.x, tr.x, bl.y, tr.y
