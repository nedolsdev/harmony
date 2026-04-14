"""Detect collisions between two colliders."""

from __future__ import annotations

from collections.abc import Callable

from core.packages.collision.collider import Collider, ColliderType
from core.packages.collision.collision import Collision
from core.packages.timing.delta_time import Singleton

type CollisionFunc = Callable[[Collider, Collider], Collision | None]


class CollisionDetector(metaclass=Singleton):
    """Detect collisions between two colliders."""

    def __init__(self) -> None:
        """Initialize the CollisionDetector with a dict of sub-detectors."""
        self.detectors: dict[tuple[ColliderType, ColliderType], CollisionFunc] = {}

    def _add_detector(
        self,
        collider_a_type: ColliderType,
        collider_b_type: ColliderType,
        func: CollisionFunc,
    ) -> None:
        """Add a specific detector between two collision types."""
        self.detectors[(collider_a_type, collider_b_type)] = func

        def get_inverse_func(func: CollisionFunc) -> CollisionFunc:
            """Get the inverse collision function of a collision function."""

            def inner(collider_a: Collider, collider_b: Collider) -> Collision | None:
                collision = func(collider_b, collider_a)
                if collision is None:
                    return None
                return collision.get_inverse()

            return inner

        # different colliders, so we also add the inverse
        if collider_a_type != collider_b_type:
            inverse_func = get_inverse_func(func)
            self.detectors[(collider_b_type, collider_a_type)] = inverse_func

    @staticmethod
    def add_detector(
        collider_a_type: ColliderType,
        collider_b_type: ColliderType,
        func: CollisionFunc,
    ) -> None:
        """Add a specific detector between two collision types."""
        CollisionDetector()._add_detector(collider_a_type, collider_b_type, func)  # noqa: SLF001

    def get_detector(self, collider_pair: tuple[Collider, Collider]) -> CollisionFunc:
        """Get the detector function for a given Collider pair."""
        type_a = collider_pair[0].get_type()
        type_b = collider_pair[1].get_type()

        detector = self.detectors.get((type_a, type_b), None)

        if detector is None:
            msg = f"Collision detection between type '{type_a}' and '{type_b}' does not exist."
            raise LookupError(msg)

        return detector

    def detect_collision(self, collider_pair: tuple[Collider, Collider]) -> Collision | None:
        """Detect collision between two colliders."""
        detector = self.get_detector(collider_pair)
        return detector(collider_pair[0], collider_pair[1])
