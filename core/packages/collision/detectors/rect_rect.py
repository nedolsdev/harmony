"""Rect/Rect collision detection."""
from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.collision.collision import Collision
from core.packages.collision.collision_detector import CollisionDetector

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

    axes: list[Vector2] = [
        a_edge1.normalize(),
        a_edge2.normalize(),
        b_edge1.normalize(),
        b_edge2.normalize(),
    ]

    for axis in axes:
        a_min, a_max = project(ap, axis)
        b_min, b_max = project(bp, axis)

        if not overlap(a_min, a_max, b_min, b_max):
            return None

    return Collision(collider_a=rect_a, collider_b=rect_b)


CollisionDetector.add_detector("rect", "rect", rect_rect_collision)  # pyright: ignore[reportArgumentType] (simplicity is worth it here)
