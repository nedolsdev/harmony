"""Polygon asset."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame
import pygame.gfxdraw

from harmony.game.asset import Asset
from harmony.game.error import InvalidArgumentCombinationError

if TYPE_CHECKING:
    from harmony.core.packages.geometry.polygon import Polygon
    from harmony.core.packages.render.color import Color


class PolygonAsset(Asset):
    """Polygon asset."""

    def __init__(
        self,
        polygon: Polygon,
        fill_color: Color | None = None,
        outline_color: Color | None = None,
        outline_width: int = 0,
        *,
        antialiased: bool = False,
    ) -> None:
        """Initialize the Polygon with a list of points."""
        # should have a fill or outline
        if fill_color is None and outline_color is None:
            msg = "No fill_color or outline_color was given. At least one must be present."
            raise InvalidArgumentCombinationError(msg)

        self.polygon = polygon
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.antialiased = antialiased

    def create_surface(self) -> pygame.Surface:
        """Create a surface for the polygon."""
        min_x, max_x, min_y, max_y = self.polygon.bounds()

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

    def copy(self) -> PolygonAsset:
        """Create a copy of the current Polygon."""
        return PolygonAsset(
            polygon=self.polygon.copy(),
            fill_color=self.fill_color,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            antialiased=self.antialiased,
        )
