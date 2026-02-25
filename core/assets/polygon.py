"""Polygon asset."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame
import pygame.gfxdraw

from core.assets.surface_asset import ScalableSurfaceAsset

if TYPE_CHECKING:
    from collections.abc import Iterable

    from game.vector2 import Vector2


class Polygon(ScalableSurfaceAsset):
    """Polygon asset."""

    def __init__(
        self,
        points: Iterable[tuple[float, float]],
        fill_color: tuple[int, int, int] | None = None,
        outline_color: tuple[int, int, int] | None = None,
        outline_width: int = 0,
        *,
        antialiased: bool = False,
    ) -> None:
        """Initialize the Polygon with a list of points."""
        # should have a fill or outline
        if fill_color is None and outline_color is None:
            msg = "No fill_color or outline_color was given. At least one must be present."
            raise ValueError(msg)

        self.local_points = list(points)
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.antialiased = antialiased

    def _create_surface(self) -> pygame.Surface:
        xs = [p[0] for p in self.local_points]
        ys = [p[1] for p in self.local_points]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = math.ceil(max_x - min_x) + 1
        height = math.ceil(max_y - min_y) + 1

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        shifted_points = [(x - min_x, y - min_y) for x, y in self.local_points]

        if self.antialiased:
            int_points = [(int(x), int(y)) for x, y in shifted_points]

            if self.fill_color:
                pygame.gfxdraw.filled_polygon(surface, int_points, self.fill_color)
                pygame.gfxdraw.aapolygon(surface, int_points, self.fill_color)

            if self.outline_color and self.outline_width > 0:
                pygame.gfxdraw.aapolygon(surface, int_points, self.outline_color)

        else:
            if self.fill_color:
                pygame.draw.polygon(surface, self.fill_color, shifted_points)

            if self.outline_color and self.outline_width > 0:
                pygame.draw.polygon(
                    surface,
                    self.outline_color,
                    shifted_points,
                    self.outline_width,
                )

        return surface

    def _get_scaled_points(self, scale: Vector2) -> list[tuple[float, float]]:
        """Return new points scaled by the given scale factor."""
        return [(x * scale.x, y * scale.y) for x, y in self.local_points]

    def get_surface_of_scale(self, scale: Vector2) -> pygame.Surface:
        """Get the surface of the polygon."""
        if scale.x <= 0 or scale.y <= 0:
            msg = "Size must be positive."
            raise ValueError(msg)

        scaled_points = self._get_scaled_points(scale)

        scaled_polygon = Polygon(
            points=scaled_points,
            fill_color=self.fill_color,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            antialiased=self.antialiased,
        )

        return scaled_polygon._create_surface()

    @classmethod
    def regular(  # noqa: PLR0913
        cls,
        sides: int,
        radius: float,
        fill_color: tuple[int, int, int] | None = None,
        outline_color: tuple[int, int, int] | None = None,
        outline_width: int = 0,
        *,
        antialiased: bool = False,
        rotation_degrees: float = 0.0,
    ) -> Polygon:
        """Create a regular n-sided polygon centered at (0, 0)."""
        number_of_sides_of_smallest_polygon = 3
        if sides < number_of_sides_of_smallest_polygon:
            msg = "A polygon must have at least 3 sides."
            raise ValueError(msg)

        points: list[tuple[float, float]] = []

        angle_offset = math.radians(rotation_degrees)

        for i in range(sides):
            angle = 2 * math.pi * i / sides + angle_offset
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append((x, y))

        return cls(
            points=points,
            fill_color=fill_color,
            outline_color=outline_color,
            outline_width=outline_width,
            antialiased=antialiased,
        )

    def copy(self) -> Polygon:
        """Create a copy of the current Polygon."""
        return Polygon(
            points=self.local_points,
            fill_color=self.fill_color,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            antialiased=self.antialiased,
        )
