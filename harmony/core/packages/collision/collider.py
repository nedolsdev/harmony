"""The underlying collider that computes collisions between two like colliders."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal, override

from harmony.core.components.transform import Transform
from harmony.core.packages.collision.collision_surface import DEFAULT_SURFACE, CollisionSurface
from harmony.core.packages.physics.rigidbody_2d import RigidBody2D
from harmony.game.behavior import Behavior
from harmony.game.dirty import Dirtyable
from harmony.game.error import MissingComponentDependencyError

if TYPE_CHECKING:
    from harmony.core.packages.collision.collision import Collision
    from harmony.core.packages.collision.collision_layer import CollisionLayer
    from harmony.core.packages.collision.collision_manager import CollisionInteraction


ColliderType = Literal["rect", "circle", "poly"]


class Collider(Behavior, Dirtyable, ABC):
    """The underlying collider that computes collisions between two like colliders."""

    def __init__(self, collision_surface: CollisionSurface | None = None) -> None:
        """Initialize the Collider."""
        super().__init__()
        self.layers: set[CollisionLayer] = set()

        self.collision_surface = collision_surface or DEFAULT_SURFACE

        self.rigid_body_2d: RigidBody2D | None = None

    @staticmethod
    @abstractmethod
    def get_type() -> ColliderType:
        """Get the type of collider (e.g. 'rect')."""

    def add_layer(self, layer: CollisionLayer) -> None:
        """Add a CollisionLayer that the Collider interacts with."""
        self.layers.add(layer)
        layer.colliders.append(self)

    def send_collision_event(self, collision: Collision, interaction: CollisionInteraction) -> None:
        """Send the collision event to the game object."""
        self.game_object.handle_collision(collision, interaction)

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        if not self.game_object.has_component(Transform):
            msg = "ColliderRect does not have necessary 'Transform' component attached."
            raise MissingComponentDependencyError(msg)

        self.transform = self.game_object.get_component(Transform)

        if self.game_object.has_component(RigidBody2D):
            self.rigid_body_2d = self.game_object.get_component(RigidBody2D)
