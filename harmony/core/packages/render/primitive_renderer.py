"""Primitive renderer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from harmony.core.assets.polygon_asset import PolygonAsset
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
                pass
            case RectRenderPrimitive():
                pass
            case CircleRenderPrimitive():
                pass
            case PolygonRenderPrimitive():
                pass
            case SpriteRenderPrimitive():
                pass

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
        asset = PolygonAsset(
            primitive.polygon,
            primitive.fill,
            outline_color=primitive.stroke.color,
            outline_width=primitive.stroke.thickness,
            antialiased=False,
        )

        poly_surface = asset.create_surface()
        primitive.material.apply(poly_surface)
        self.surface.blit(poly_surface, primitive.polygon.top_left())

    def _render_sprite(self, primitive: SpriteRenderPrimitive) -> None:
        raise NotImplementedError
