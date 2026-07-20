"""A collision between two RigidBody2D."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.collision.collision import Collision

if TYPE_CHECKING:
    from harmony.core.packages.collision.collider import Collider
    from harmony.core.packages.collision.contact import Contact
    from harmony.core.packages.physics.rigidbody_2d import RigidBody2D


class CollisionRigidBody2D(Collision):
    """A collision between two RigidBody2D."""

    contact: Contact

    def __init__(
        self,
        collider_a: Collider,
        collider_b: Collider,
        contact: Contact,
        rigid_body_a: RigidBody2D,
        rigid_body_b: RigidBody2D,
    ) -> None:
        """Initialize the CollisionRigidBody2D."""
        super().__init__(collider_a, collider_b, contact)
        self.rigid_body_a = rigid_body_a
        self.rigid_body_b = rigid_body_b
