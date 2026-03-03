"""Polygon asset."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame
import pygame.gfxdraw

from core.assets.surface_asset import ScalableSurfaceAsset

if TYPE_CHECKING:
    from core.packages.geometry.polygon import Polygon
    from game.vector2 import Vector2


class PolygonAsset(ScalableSurfaceAsset):
    """Polygon asset."""

    def __init__(
        self,
        polygon: Polygon,
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

        self.polygon = polygon
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.antialiased = antialiased

    def _create_surface(self) -> pygame.Surface:
        xs = [p.x for p in self.polygon.points]
        ys = [p.y for p in self.polygon.points]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = math.ceil(max_x - min_x) + 1
        height = math.ceil(max_y - min_y) + 1

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        shifted_points = [(point.x - min_x, point.y - min_y) for point in self.polygon.points]

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

    def get_surface_of_scale(self, scale: Vector2) -> pygame.Surface:
        """Get the surface of the polygon."""
        if scale.x <= 0 or scale.y <= 0:
            msg = "Size must be positive."
            raise ValueError(msg)

        scaled_polygon = PolygonAsset(
            polygon=self.polygon.scale(scale),
            fill_color=self.fill_color,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            antialiased=self.antialiased,
        )

        return scaled_polygon._create_surface()

    def copy(self) -> PolygonAsset:
        """Create a copy of the current Polygon."""
        return PolygonAsset(
            polygon=self.polygon.copy(),
            fill_color=self.fill_color,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            antialiased=self.antialiased,
        )
