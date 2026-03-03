"""The line segment geometry primitive."""

from __future__ import annotations

import math
from typing import override

from core.packages.geometry.geometry import Geometry, Rotatable, ScalableVector2
from game.vector2 import Vector2


class LineSegment(Geometry, ScalableVector2, Rotatable):
    """The line segment geometry primitive."""

    def __init__(self, start: Vector2, end: Vector2) -> None:
        """Initialize the LineSegment with a start and end point."""
        super().__init__()
        self.start = start
        self.end = end

    @override
    def copy(self) -> LineSegment:
        return LineSegment(self.start.copy(), self.end.copy())

    @classmethod
    def from_angle_and_length(cls, start: Vector2, angle: float, length: float) -> LineSegment:
        """Create a LineSegment from a start point, angle (in radians), and length."""
        end = Vector2(start.x + math.cos(angle) * length, start.y + math.sin(angle) * length)
        return cls(start.copy(), end)

    @override
    def scale(self, factor: Vector2) -> LineSegment:
        return LineSegment(self.start * factor, self.end * factor)

    @override
    def rotate_radians(self, radians: float) -> LineSegment:
        return LineSegment(
            self.start.rotate(radians),
            self.end.rotate(radians),
        )
