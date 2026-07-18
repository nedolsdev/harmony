"""Builds collision manifolds for convex shapes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.collision.manifold.core import Manifold
from harmony.core.packages.collision.manifold.edge import Edge

if TYPE_CHECKING:
    from harmony.core.packages.collision.collider_rect import ColliderRect
    from harmony.core.packages.geometry.vector2 import Vector2


class ManifoldBuilder:
    """Builds collision manifolds for convex shapes."""

    @staticmethod
    def build_rect_rect(rect_a: ColliderRect, rect_b: ColliderRect, normal: Vector2, penetration: float) -> Manifold:
        """Build collision manifold between two rectangle colliders."""
        a_pts = rect_a.world_rect.points
        b_pts = rect_b.world_rect.points

        # ensure consistent direction (A -> B)
        center_dir = rect_b.world_rect.center - rect_a.world_rect.center
        if center_dir.dot(normal) < 0.0:
            normal = -normal

        ref_pts, inc_pts = ManifoldBuilder._choose_reference_and_incident(a_pts, b_pts, normal)

        ref_edge = ManifoldBuilder._best_face(ref_pts, normal)
        inc_edge = ManifoldBuilder._best_face(inc_pts, -normal)

        ref_normal = normal
        ref_point = ref_edge.a
        ref_d = ref_normal.dot(ref_point)

        clipped = ManifoldBuilder._clip_polygon([inc_edge.a, inc_edge.b], ref_normal, ref_d)

        contacts = ManifoldBuilder._extract_contacts(clipped, ref_normal, ref_point)

        return Manifold(
            normal=normal,
            penetration=penetration,
            contacts=contacts,
        )

    @staticmethod
    def _choose_reference_and_incident(
        a: list[Vector2],
        b: list[Vector2],
        normal: Vector2,
    ) -> tuple[list[Vector2], list[Vector2]]:
        # shape whose face normal aligns most with collision normal is reference
        a_align = ManifoldBuilder._max_face_alignment(a, normal)
        b_align = ManifoldBuilder._max_face_alignment(b, normal)

        if a_align >= b_align:
            return a, b
        return b, a

    @staticmethod
    def _best_face(points: list[Vector2], normal: Vector2) -> Edge:
        best_dot = float("-inf")
        best_edge: Edge | None = None

        for i in range(4):
            e = Edge(points[i], points[(i + 1) % 4])
            d = e.normal.dot(normal)

            if d > best_dot:
                best_dot = d
                best_edge = e

        if best_edge is None:
            msg = "Could not find a suitable edge. Something went wrong."
            raise ValueError(msg)

        return best_edge

    @staticmethod
    def _max_face_alignment(points: list[Vector2], normal: Vector2) -> float:
        best = float("-inf")

        for i in range(4):
            e = Edge(points[i], points[(i + 1) % 4])
            best = max(best, e.normal.dot(normal))

        return best

    @staticmethod
    def _clip_polygon(
        pts: list[Vector2],
        normal: Vector2,
        d: float,
    ) -> list[Vector2]:
        def dist(p: Vector2) -> float:
            return p.dot(normal) - d

        out: list[Vector2] = []
        p1 = pts[0]
        p2 = pts[1]

        d1 = dist(p1)
        d2 = dist(p2)

        if d1 <= 0:
            out.append(p1)
        if d2 <= 0:
            out.append(p2)

        if d1 * d2 < 0:
            t = d1 / (d1 - d2)
            inter = p1 + (p2 - p1) * t
            out.append(inter)

        return out

    @staticmethod
    def _extract_contacts(
        pts: list[Vector2],
        normal: Vector2,
        ref_point: Vector2,
    ) -> list[Vector2]:
        contacts: list[Vector2] = []

        for p in pts:
            if normal.dot(p - ref_point) <= 0.0:
                contacts.append(p)  # noqa: PERF401

        return contacts
