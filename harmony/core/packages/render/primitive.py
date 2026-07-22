"""A render primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.game.material import Material, NoMaterial

if TYPE_CHECKING:
    from harmony.core.assets.sprite_image import SpriteImage
    from harmony.core.packages.geometry.circle import Circle
    from harmony.core.packages.geometry.geometry import Geometry
    from harmony.core.packages.geometry.line_segment import LineSegment
    from harmony.core.packages.geometry.polygon import Polygon
    from harmony.core.packages.geometry.rectangle import Rectangle


class RenderPrimitive:
    """A render primitive."""

    def __init__(self, material: Material | None = None) -> None:
        """Initialize the RenderPrimitive."""
        self.material = material or NoMaterial()


class GeometryRenderPrimitive(RenderPrimitive):
    """A geometry render primitive."""

    def __init__(self, geometry: Geometry, material: Material | None = None) -> None:
        """Initialize the GeometryRenderPrimitive."""
        super().__init__(material)
        self.geometry = geometry


class Line2DRenderPrimitive(GeometryRenderPrimitive):
    """A Line2D render primitive."""

    def __init__(self, line_segment: LineSegment, material: Material | None = None) -> None:
        """Initialize the Line2DRenderPrimitive."""
        super().__init__(line_segment, material)


class PolygonRenderPrimitive(GeometryRenderPrimitive):
    """A Polygon render primitive."""

    def __init__(self, polygon: Polygon, material: Material | None = None) -> None:
        """Initialize the PolygonRenderPrimitive."""
        super().__init__(polygon, material)
        self.polygon: Polygon = polygon


class RectRenderPrimitive(PolygonRenderPrimitive):
    """A RectRenderPrimitive render primitive."""

    def __init__(self, rect: Rectangle, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(rect, material)
        self.rect = rect


class CircleRenderPrimitive(GeometryRenderPrimitive):
    """A CircleRenderPrimitive render primitive."""

    def __init__(self, circle: Circle, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(circle, material)
        self.circle = circle


class SpriteRenderPrimitive(RenderPrimitive):
    """A sprite render primitive."""

    def __init__(self, sprite: SpriteImage, material: Material | None = None) -> None:
        """Initialize the SpriteRenderPrimitive."""
        super().__init__(material)
        self.sprite = sprite
