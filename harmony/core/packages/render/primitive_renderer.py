"""Primitive renderer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.render.primitive import (
    CircleRenderPrimitive,
    Line2DRenderPrimitive,
    PolygonRenderPrimitive,
    RectRenderPrimitive,
    SpriteRenderPrimitive,
)

if TYPE_CHECKING:
    import pygame

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
        raise NotImplementedError

    def _render_rect(self, primitive: RectRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_circle(self, primitive: CircleRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_polygon(self, primitive: PolygonRenderPrimitive) -> None:
        raise NotImplementedError

    def _render_sprite(self, primitive: SpriteRenderPrimitive) -> None:
        raise NotImplementedError
