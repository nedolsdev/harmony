"""Transform utils for different geometries."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from harmony.core.packages.geometry.circle import Circle
from harmony.core.packages.geometry.line_segment import LineSegment
from harmony.core.packages.geometry.polygon import Polygon
from harmony.core.packages.geometry.rectangle import Rectangle

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform


def transform_polygon(polygon: Polygon, transform: Transform) -> Polygon:
    """Transform Polygon."""
    return Polygon([transform.transform_point(p) for p in polygon.points])


def transform_line_segment(line_segment: LineSegment, transform: Transform) -> LineSegment:
    """Transform LineSegment."""
    return LineSegment(
        transform.transform_point(line_segment.start),
        transform.transform_point(line_segment.end),
    )


def transform_rectangle(rect: Rectangle, transform: Transform) -> Rectangle:
    """Return a new Rectangle transformed by the given Transform."""
    world_center = transform.transform_point(rect.center)

    world_rotation = rect.rotation_radians + transform.world_rotation

    world_width = rect.width * transform.world_scale.x
    world_height = rect.height * transform.world_scale.y

    return Rectangle(
        width=world_width,
        height=world_height,
        center=world_center,
        rotation_degrees=math.degrees(world_rotation),
    )


def transform_circle(circle: Circle, transform: Transform) -> Circle:
    """Return a new Circle transformed by the given Transform."""
    world_center = transform.transform_point(circle.center)

    scale_x, scale_y = transform.world_scale.x, transform.world_scale.y

    # TODO: Support ellipses  # noqa: TD003
    # for now we just take the average (mega scuffed but whatever)
    world_radius = circle.radius * (scale_x + scale_y) / 2

    return Circle(radius=world_radius, center=world_center)
