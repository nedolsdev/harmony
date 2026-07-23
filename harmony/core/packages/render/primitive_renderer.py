"""Primitive renderer."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame
import pygame.gfxdraw

from harmony.core.packages.render.primitive import (
    CircleRenderPrimitive,
    Line2DRenderPrimitive,
    PolygonRenderPrimitive,
    RectRenderPrimitive,
    SpriteRenderPrimitive,
)

if TYPE_CHECKING:
    from harmony.core.packages.render.primitive import RenderPrimitive


class PrimitiveRenderer:
    """Primitive renderer."""

    def render_primitives(self, primitives: list[RenderPrimitive]) -> None:
        """Render the primitives."""
        for primitive in primitives:
            self._render_primitive(primitive)

    def _render_primitive(self, primitive: RenderPrimitive) -> None:
        match primitive:
            case Line2DRenderPrimitive():
                self._render_line(primitive)
            case RectRenderPrimitive():
                self._render_rect(primitive)
            case CircleRenderPrimitive():
                self._render_circle(primitive)
            case PolygonRenderPrimitive():
                self._render_polygon(primitive)
            case SpriteRenderPrimitive():
                self._render_sprite(primitive)

    def _render_line(self, primitive: Line2DRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_rect(self, primitive: RectRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_circle(self, primitive: CircleRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_polygon(self, primitive: PolygonRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_sprite(self, primitive: SpriteRenderPrimitive) -> None:
        raise NotImplementedError


class PygamePrimitiveRenderer(PrimitiveRenderer):
    """Primitive renderer for rendering a Pygame game."""

    def __init__(self, surface: pygame.Surface) -> None:
        """Initialize the PygamePrimitiveRenderer."""
        super().__init__()
        self.surface = surface

    def _render_line(self, primitive: Line2DRenderPrimitive) -> None:
        line_surface = pygame.Surface(primitive.size(), pygame.SRCALPHA)

        pygame.draw.line(
            line_surface,
            (255, 255, 255, 255),
            primitive.segment.start.as_tuple(),
            primitive.segment.end.as_tuple(),
            primitive.thickness,
        )

        primitive.material.apply(line_surface)
        self.surface.blit(line_surface, primitive.segment.top_left())

    def _render_rect(self, primitive: RectRenderPrimitive) -> None:
        rect = primitive.rect

        width = int(rect.width)
        height = int(rect.height)

        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        if primitive.fill is not None:
            pygame.draw.rect(
                rect_surface,
                primitive.fill,
                pygame.Rect(0, 0, width, height),
            )

        if primitive.stroke.thickness > 0:
            pygame.draw.rect(
                rect_surface,
                primitive.stroke.color,
                pygame.Rect(0, 0, width, height),
                primitive.stroke.thickness,
            )

        primitive.material.apply(rect_surface)

        self.surface.blit(rect_surface, rect.top_left())

    def _render_circle(self, primitive: CircleRenderPrimitive) -> None:
        radius = int(primitive.circle.radius)
        diameter = radius * 2

        circle_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        center = (radius, radius)

        if primitive.fill is not None:
            pygame.draw.circle(
                circle_surface,
                primitive.fill,
                center,
                radius,
            )

        if primitive.stroke.thickness > 0:
            pygame.draw.circle(
                circle_surface,
                primitive.stroke.color,
                center,
                radius,
                primitive.stroke.thickness,
            )

        primitive.material.apply(circle_surface)

        self.surface.blit(
            circle_surface,
            (
                primitive.circle.center.x - radius,
                primitive.circle.center.y - radius,
            ),
        )

    def _render_polygon(self, primitive: PolygonRenderPrimitive) -> None:
        poly_surface = self._compute_pygame_polygon_surface(primitive)
        primitive.material.apply(poly_surface)
        self.surface.blit(poly_surface, primitive.polygon.top_left())

    def _compute_pygame_polygon_surface(self, primitive: PolygonRenderPrimitive) -> pygame.Surface:
        """Create a surface for the polygon."""
        polygon = primitive.polygon
        antialiased = primitive.antialiased
        fill_color = primitive.fill
        outline_color = primitive.stroke.color
        outline_width = primitive.stroke.thickness

        min_x, max_x, min_y, max_y = polygon.bounds()

        width = math.ceil(max_x - min_x) + 1
        height = math.ceil(max_y - min_y) + 1

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        shifted_points = [(point.x - min_x, point.y - min_y) for point in polygon.points]

        if antialiased:
            int_points = [(int(x), int(y)) for x, y in shifted_points]

            if fill_color:
                pygame.gfxdraw.filled_polygon(surface, int_points, fill_color)
                pygame.gfxdraw.aapolygon(surface, int_points, fill_color)

            if outline_color and outline_width > 0:
                pygame.gfxdraw.aapolygon(surface, int_points, outline_color)

        else:
            if fill_color:
                pygame.draw.polygon(surface, fill_color, shifted_points)

            if outline_color and outline_width > 0:
                pygame.draw.polygon(
                    surface,
                    outline_color,
                    shifted_points,
                    outline_width,
                )

        return surface

    def _render_sprite(self, primitive: SpriteRenderPrimitive) -> None:
        raise NotImplementedError
