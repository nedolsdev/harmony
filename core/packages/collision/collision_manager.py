"""The collision manager controls which collisions need to be checked."""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from core.packages.collision.collision import Collision
from core.packages.collision.collision_detector import CollisionDetector
from core.packages.collision.detectors.rect_rect import rect_rect_collision
from core.packages.collision.upgrade import upgrade_collision

if TYPE_CHECKING:
    from core.packages.collision.collider import Collider
    from core.packages.collision.collision_layer import CollisionLayer
    from core.packages.collision.collision_rule import CollisionRule


class CollisionInteraction(Enum):
    """Enum for CollisionInteraction between two Colliders."""

    ENTER = auto()
    STAY = auto()
    EXIT = auto()


class CollisionManager:
    """The collision manager controls which collisions need to be checked."""

    def __init__(self) -> None:
        """Initialize the CollisionManager."""
        self.rules: dict[CollisionLayer, CollisionRule] = {}
        self.layers: dict[str, CollisionLayer] = {}
        self.detector = CollisionDetector()

        # support rect-rect collision
        self.detector.add_detector("rect", "rect", rect_rect_collision)  # ty:ignore[invalid-argument-type]

        # colliders pairs from last frame
        self.last_frame_pairs: set[tuple[Collider, Collider]] = set()

    def detect_collisions(self) -> list[Collision]:
        """Detect collisions."""
        collisions: list[Collision] = []

        for rule in self.rules.values():
            pairs = rule.get_all_collider_pairs()

            for pair in pairs:
                collision_func = self.detector.get_detector(pair)

                left = pair[0]
                right = pair[1]

                collision = collision_func(left, right)
                if collision is not None:
                    collisions.append(upgrade_collision(collision))

        return collisions

    def dispatch_events(self, collisions: list[Collision]) -> None:
        """Dispatch collision events."""
        collider_pairs: set[tuple[Collider, Collider]] = set()

        for collision in collisions:
            left = collision.collider_a
            right = collision.collider_b

            collider_pairs.add((left, right))

            collided_last_frame = (left, right) in self.last_frame_pairs
            collision_type = CollisionInteraction.STAY if collided_last_frame else CollisionInteraction.ENTER

            left.send_collision_event(collision, collision_type)
            right.send_collision_event(collision.get_inverse(), collision_type)

        for pair in self.last_frame_pairs:
            if pair not in collider_pairs:
                left, right = pair

                collision = Collision(left, right, None)

                left.send_collision_event(collision, CollisionInteraction.EXIT)
                right.send_collision_event(collision.get_inverse(), CollisionInteraction.EXIT)

        self.last_frame_pairs = collider_pairs

    def add_rule(self, rule: CollisionRule) -> None:
        """Add a CollisionRule."""
        self.rules[rule.layer] = rule

    def add_collision_layer(self, layer: CollisionLayer) -> None:
        """Add a CollisionLayer."""
        self.layers[layer.name] = layer

    def get_layer(self, name: str) -> CollisionLayer | None:
        """Get a CollisionLayer with name."""
        return self.layers.get(name, None)
