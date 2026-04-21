"""Detector utility that gets RigidBody2D collision if available."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.collision.rigidbody_collision import CollisionRigidBody2D

if TYPE_CHECKING:
    from core.packages.collision.collision import Collision


def upgrade_collision(collision: Collision) -> Collision:
    """Upgrade the collision to RigidBody2DCollision if possible."""
    collider_a = collision.collider_a
    collider_b = collision.collider_b

    if collider_a.rigid_body_2d is not None and collider_b.rigid_body_2d is not None and collision.contact is not None:
        return CollisionRigidBody2D(
            collider_a,
            collider_b,
            collision.contact,
            collider_a.rigid_body_2d,
            collider_b.rigid_body_2d,
        )
    return collision
