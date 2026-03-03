"""The rectangle geometry primitive."""

from __future__ import annotations

import math
from typing import override

from core.packages.geometry.polygon import Polygon
from game.vector2 import Vector2


class Rectangle(Polygon):
    """The rectangle geometry primitive (extends Polygon)."""

    def __init__(
        self,
        width: float,
        height: float,
        center: Vector2,
        *,
        rotation_degrees: float = 0.0,
    ) -> None:
        """Initialize a rectangle given width, height, center and optional rotation in radians."""
        self.width = width
        self.height = height
        self.center = center
        self.rotation_radians = math.radians(rotation_degrees)

        half_width, half_height = width / 2, height / 2
        corners = [
            Vector2(-half_width, -half_height),
            Vector2(half_width, -half_height),
            Vector2(half_width, half_height),
            Vector2(-half_width, half_height),
        ]

        points = [
            Vector2(
                corner.x * math.cos(self.rotation_radians) - corner.y * math.sin(self.rotation_radians) + center.x,
                corner.x * math.sin(self.rotation_radians) + corner.y * math.cos(self.rotation_radians) + center.y,
            )
            for corner in corners
        ]

        super().__init__(points=points)

    @override
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    @override
    def area(self) -> float:
        return self.width * self.height

    @override
    def contains_point(self, point: Vector2) -> bool:
        dx = point.x - self.center.x
        dy = point.y - self.center.y

        cos_r = math.cos(-self.rotation_radians)
        sin_r = math.sin(-self.rotation_radians)
        local_x = dx * cos_r - dy * sin_r
        local_y = dx * sin_r + dy * cos_r

        hw, hh = self.width / 2, self.height / 2
        return -hw <= local_x <= hw and -hh <= local_y <= hh

    @override
    def copy(self) -> Rectangle:
        return Rectangle(
            self.width,
            self.height,
            self.center.copy(),
            rotation_degrees=math.degrees(self.rotation_radians),
        )

    @override
    def scale(self, factor: Vector2) -> Rectangle:
        return Rectangle(
            self.width * factor.x,
            self.height * factor.y,
            self.center.copy(),
            rotation_degrees=math.degrees(self.rotation_radians),
        )

    @override
    def rotate_radians(self, radians: float) -> Rectangle:
        rotation = radians + self.rotation_radians
        return Rectangle(self.width, self.height, self.center.copy(), rotation_degrees=math.degrees(rotation))
