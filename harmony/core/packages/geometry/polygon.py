"""The polygon geometry primitive (extends Shape)."""

from __future__ import annotations

import math
from typing import override

from harmony.core.packages.geometry.geometry import Rotatable, ScalableVector2
from harmony.core.packages.geometry.shape import Shape
from harmony.core.packages.geometry.vector2 import Vector2


class Polygon(Shape, ScalableVector2, Rotatable):
    """The polygon geometry primitive (extends Shape)."""

    number_of_sides_of_smallest_polygon = 3

    def __init__(self, points: list[Vector2]) -> None:
        """Initialize the Polygon with a set of points."""
        sides = len(points)
        self._validate_sides(sides)
        super().__init__(sides)
        self.points = points

    @classmethod
    def _validate_sides(cls, sides: int) -> None:
        """Raise an error if sides are fewer than the minimum allowed."""
        if sides < cls.number_of_sides_of_smallest_polygon:
            msg = f"A polygon must have at least {cls.number_of_sides_of_smallest_polygon} sides."
            raise ValueError(msg)

    @classmethod
    def regular(
        cls,
        sides: int,
        radius: float,
        rotation_degrees: float = 0.0,
    ) -> Polygon:
        """Create a regular n-sided polygon centered at (0, 0)."""
        cls._validate_sides(sides)

        points: list[Vector2] = []
        angle_offset = math.radians(rotation_degrees)

        for i in range(sides):
            angle = 2 * math.pi * i / sides + angle_offset
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append(Vector2(x, y))

        return cls(points=points)

    @override
    def perimeter(self) -> float:
        """Calculate the perimeter by summing distances between consecutive points."""
        perimeter = 0.0
        num_points = len(self.points)
        for i in range(num_points):
            perimeter += self.points[i].distance_to(self.points[(i + 1) % num_points])
        return perimeter

    @override
    def area(self) -> float:
        """Calculate the area using the shoelace formula."""
        num_points = len(self.points)
        sum1, sum2 = 0.0, 0.0
        for i in range(num_points):
            x0, y0 = self.points[i].x, self.points[i].y
            x1, y1 = self.points[(i + 1) % num_points].x, self.points[(i + 1) % num_points].y
            sum1 += x0 * y1
            sum2 += y0 * x1
        return abs(sum1 - sum2) / 2

    @override
    def contains_point(self, point: Vector2) -> bool:
        """Determine if a point is inside the polygon using the ray casting method."""
        count = 0
        num_points = len(self.points)
        for i in range(num_points):
            a = self.points[i]
            b = self.points[(i + 1) % num_points]
            if ((a.y > point.y) != (b.y > point.y)) and (
                point.x < (b.x - a.x) * (point.y - a.y) / (b.y - a.y + 1e-10) + a.x
            ):
                count += 1
        return count % 2 == 1

    @override
    def copy(self) -> Polygon:
        """Return a deep copy of the polygon."""
        return Polygon([Vector2(p.x, p.y) for p in self.points])

    @override
    def scale(self, factor: Vector2) -> Polygon:
        """Return a scaled copy of the polygon."""
        return Polygon([point * factor for point in self.points])

    @override
    def rotate_radians(self, radians: float) -> Polygon:
        """Return a rotated copy of the polygon (around the origin)."""
        return Polygon([point.rotate(radians) for point in self.points])

    @override
    def bounds(self) -> tuple[float, float, float, float]:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return min(xs), max(xs), min(ys), max(ys)
