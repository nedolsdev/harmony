"""A render primitive."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from harmony.game.material import Material, NoMaterial

if TYPE_CHECKING:
    from harmony.core.assets.sprite_image import SpriteImage
    from harmony.core.packages.geometry.circle import Circle
    from harmony.core.packages.geometry.geometry import Geometry
    from harmony.core.packages.geometry.line_segment import LineSegment
    from harmony.core.packages.geometry.polygon import Polygon
    from harmony.core.packages.geometry.rectangle import Rectangle
    from harmony.core.packages.geometry.shape import Shape
    from harmony.core.packages.geometry.vector2 import Vector2
    from harmony.core.packages.render.color import Color


@dataclass(slots=True)
class Stroke:
    """Shape stroke."""

    thickness: int = 1
    color: Color = (0, 0, 0)


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

    def __init__(
        self,
        line_segment: LineSegment,
        thickness: int,
        material: Material | None = None,
    ) -> None:
        """Initialize the Line2DRenderPrimitive."""
        super().__init__(line_segment, material)
        self.thickness = thickness


class ShapeRenderPrimitive(GeometryRenderPrimitive):
    """A shape render primitive."""

    def __init__(self, shape: Shape, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the PolygonRenderPrimitive."""
        super().__init__(shape, material)
        self.polygon = shape
        self.fill = fill
        self.stroke = stroke


class PolygonRenderPrimitive(ShapeRenderPrimitive):
    """A Polygon render primitive."""

    def __init__(self, polygon: Polygon, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the PolygonRenderPrimitive."""
        super().__init__(polygon, fill, stroke, material)
        self.polygon: Polygon = polygon


class RectRenderPrimitive(PolygonRenderPrimitive):
    """A RectRenderPrimitive render primitive."""

    def __init__(self, rect: Rectangle, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(rect, fill, stroke, material)
        self.rect = rect


class CircleRenderPrimitive(ShapeRenderPrimitive):
    """A CircleRenderPrimitive render primitive."""

    def __init__(self, circle: Circle, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(circle, fill, stroke, material)
        self.circle = circle


class SpriteRenderPrimitive(RenderPrimitive):
    """A sprite render primitive."""

    def __init__(
        self,
        sprite: SpriteImage,
        position: Vector2,
        rotation: float,
        material: Material | None = None,
    ) -> None:
        """Initialize the SpriteRenderPrimitive."""
        super().__init__(material)
        self.sprite = sprite
        self.position = position
        self.rotation = rotation
