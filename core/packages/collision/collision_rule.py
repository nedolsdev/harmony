"""A CollisionRule defines which other layers a CollisionLayer can interact with."""

from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.collision.collider import Collider
    from core.packages.collision.collision_grouper import CollisionGrouper
    from core.packages.collision.collision_layer import CollisionLayer


class CollisionRule:
    """A CollisionRule defines which other layers a CollisionLayer can interact with."""

    def __init__(
        self,
        layer: CollisionLayer,
        grouper: CollisionGrouper,
        *,
        can_collide_with_self: bool = False,
    ) -> None:
        """Initialize the CollisionRule with the target layer."""
        self.layer = layer
        self.grouper = grouper
        self.collision_layers: set[CollisionLayer] = set()
        if can_collide_with_self:
            self.add_collision_layer(layer)

    def add_collision_layer(self, layer: CollisionLayer) -> None:
        """Add a CollisionLayer to allows collisions to the rule's layer."""
        self.collision_layers.add(layer)

    def get_all_collider_pairs(self) -> list[tuple[Collider, Collider]]:
        """Get all ColliderPairs possible for the given CollisionRule."""
        pairs: list[tuple[Collider, Collider]] = []

        for layer in self.collision_layers:
            if layer is self.layer:
                # we just want the combinations within the layer
                pairs.extend(combinations(layer.colliders, 2))
            else:
                # otherwise we can just match all pairs
                for left in self.layer.colliders:
                    for right in layer.colliders:
                        pairs.append((left, right))  # noqa: PERF401

        return pairs
