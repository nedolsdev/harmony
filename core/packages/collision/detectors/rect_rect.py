"""Rect/Rect collision detection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.collision.collision import Collision
from core.packages.collision.contact import Contact

if TYPE_CHECKING:
    from core.packages.collision.collider_rect import ColliderRect
    from core.packages.geometry.vector2 import Vector2


def rect_rect_collision(rect_a: ColliderRect, rect_b: ColliderRect) -> Collision | None:
    """Get rect/rect collision if exists."""

    def project(points: list[Vector2], axis: Vector2) -> tuple[float, float]:
        """Project points onto an axis."""
        projections = [p.dot(axis) for p in points]
        return min(projections), max(projections)

    def overlap(a_min: float, a_max: float, b_min: float, b_max: float) -> bool:
        """Check if two 1D intervals overlap."""
        return not (a_max < b_min or b_max < a_min)

    a = rect_a.world_rect
    b = rect_b.world_rect

    ap: list[Vector2] = a.points
    bp: list[Vector2] = b.points

    a_edge1: Vector2 = ap[1] - ap[0]
    a_edge2: Vector2 = ap[3] - ap[0]

    b_edge1: Vector2 = bp[1] - bp[0]
    b_edge2: Vector2 = bp[3] - bp[0]

    # SAT
    axes: list[Vector2] = [
        a_edge1.perpendicular().normalize(),
        a_edge2.perpendicular().normalize(),
        b_edge1.perpendicular().normalize(),
        b_edge2.perpendicular().normalize(),
    ]

    min_overlap: float = float("inf")
    smallest_axis: Vector2 | None = None

    for axis in axes:
        a_min, a_max = project(ap, axis)
        b_min, b_max = project(bp, axis)

        if not overlap(a_min, a_max, b_min, b_max):
            return None

        overlap_depth: float = min(a_max, b_max) - max(a_min, b_min)

        if overlap_depth < min_overlap:
            min_overlap = overlap_depth
            smallest_axis = axis

    if smallest_axis is None:
        return None

    # ensure normal points from A to B
    center_a: Vector2 = a.center
    center_b: Vector2 = b.center

    direction: Vector2 = center_b - center_a
    if direction.dot(smallest_axis) < 0.0:
        smallest_axis = -smallest_axis

    # simple single contact point
    # TODO: Improve with clipping to have multiple points  # noqa: TD003
    contact_point: Vector2 = (center_a + center_b) * 0.5

    restitution: float = min(rect_a.collision_surface.restitution, rect_b.collision_surface.restitution)
    static_friction: float = (
        rect_a.collision_surface.static_friction * rect_b.collision_surface.static_friction
    ) ** 0.5
    dynamic_friction: float = (
        rect_a.collision_surface.dynamic_friction * rect_b.collision_surface.dynamic_friction
    ) ** 0.5

    contact = Contact(
        normal=smallest_axis,
        penetration=min_overlap,
        contact_points=[contact_point],
        restitution=restitution,
        static_friction=static_friction,
        dynamic_friction=dynamic_friction,
    )

    return Collision(
        collider_a=rect_a,
        collider_b=rect_b,
        contact=contact,
    )
