"""A render primitive."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, override

from harmony.core.packages.geometry.transform import (
    transform_circle,
    transform_line_segment,
    transform_polygon,
    transform_rectangle,
)
from harmony.game.material import Material, NoMaterial

if TYPE_CHECKING:
    from pygame import Font

    from harmony.core.assets.sprite_image import SpriteImage
    from harmony.core.components.transform import Transform
    from harmony.core.packages.geometry.circle import Circle
    from harmony.core.packages.geometry.geometry import Geometry
    from harmony.core.packages.geometry.line_segment import LineSegment
    from harmony.core.packages.geometry.polygon import Polygon
    from harmony.core.packages.geometry.rectangle import Rectangle
    from harmony.core.packages.geometry.shape import Shape
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

    def transform(self, transform: Transform) -> Self:
        """Transform the render primitive."""
        raise NotImplementedError

    def bounds(self) -> tuple[float, float, float, float]:
        """Get the rectangular bounds of the geometry (min_x, max_x, min_y, max_y)."""
        raise NotImplementedError

    def size(self) -> tuple[float, float]:
        """Get the size of the render primitive."""
        raise NotImplementedError


class GeometryRenderPrimitive(RenderPrimitive):
    """A geometry render primitive."""

    def __init__(self, geometry: Geometry, material: Material | None = None) -> None:
        """Initialize the GeometryRenderPrimitive."""
        super().__init__(material)
        self.geometry = geometry

    @override
    def bounds(self) -> tuple[float, float, float, float]:
        return self.geometry.bounds()

    @override
    def size(self) -> tuple[float, float]:
        return self.geometry.size()


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
        self.segment = line_segment

    @override
    def transform(self, transform: Transform) -> Line2DRenderPrimitive:
        return Line2DRenderPrimitive(
            transform_line_segment(self.segment, transform),
            self.thickness,
            self.material,
        )


class ShapeRenderPrimitive(GeometryRenderPrimitive):
    """A shape render primitive."""

    def __init__(self, shape: Shape, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the PolygonRenderPrimitive."""
        super().__init__(shape, material)
        self.shape = shape
        self.fill = fill
        self.stroke = stroke


class PolygonRenderPrimitive(ShapeRenderPrimitive):
    """A Polygon render primitive."""

    def __init__(
        self,
        polygon: Polygon,
        fill: Color,
        stroke: Stroke,
        material: Material | None = None,
        *,
        antialiased: bool = False,
    ) -> None:
        """Initialize the PolygonRenderPrimitive."""
        super().__init__(polygon, fill, stroke, material)
        self.polygon: Polygon = polygon
        self.antialiased = antialiased

    @override
    def transform(self, transform: Transform) -> PolygonRenderPrimitive:
        return PolygonRenderPrimitive(
            transform_polygon(self.polygon, transform),
            self.fill,
            self.stroke,
            self.material,
            antialiased=self.antialiased,
        )


class RectRenderPrimitive(PolygonRenderPrimitive):
    """A RectRenderPrimitive render primitive."""

    def __init__(self, rect: Rectangle, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(rect, fill, stroke, material)
        self.rect = rect

    @override
    def transform(self, transform: Transform) -> RectRenderPrimitive:
        return RectRenderPrimitive(
            transform_rectangle(self.rect, transform),
            self.fill,
            self.stroke,
            self.material,
        )


class CircleRenderPrimitive(ShapeRenderPrimitive):
    """A CircleRenderPrimitive render primitive."""

    def __init__(self, circle: Circle, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize the RectRenderPrimitive."""
        super().__init__(circle, fill, stroke, material)
        self.circle = circle

    @override
    def transform(self, transform: Transform) -> CircleRenderPrimitive:
        return CircleRenderPrimitive(
            transform_circle(self.circle, transform),
            self.fill,
            self.stroke,
            self.material,
        )


class SpriteRenderPrimitive(RenderPrimitive):
    """A sprite render primitive."""

    def __init__(
        self,
        sprite: SpriteImage,
        rect: Rectangle,
        material: Material | None = None,
    ) -> None:
        """Initialize the SpriteRenderPrimitive."""
        super().__init__(material)
        self.sprite = sprite
        self.rect = rect

    @override
    def transform(self, transform: Transform) -> SpriteRenderPrimitive:
        return SpriteRenderPrimitive(
            self.sprite,
            transform_rectangle(self.rect, transform),
        )

    @override
    def bounds(self) -> tuple[float, float, float, float]:
        return self.rect.bounds()

    @override
    def size(self) -> tuple[float, float]:
        return self.rect.size()


class TextRenderPrimitive(RenderPrimitive):
    """A text render primitive."""

    def __init__(
        self,
        content: str,
        font: Font,
        color: Color,
        rect: Rectangle,
        material: Material | None = None,
    ) -> None:
        """Initialize the SpriteRenderPrimitive."""
        super().__init__(material)
        self.content = content
        self.font = font
        self.color = color
        self.rect = rect

    @override
    def transform(self, transform: Transform) -> TextRenderPrimitive:
        # for now we assume screen space so we don't need to transform
        # TODO: Support world space UI  # noqa: TD003
        return TextRenderPrimitive(
            self.content,
            self.font,
            self.color,
            self.rect,
            self.material,
        )

    @override
    def bounds(self) -> tuple[float, float, float, float]:
        return self.rect.bounds()

    @override
    def size(self) -> tuple[float, float]:
        return self.rect.size()
