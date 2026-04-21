"""Physics manager runs the physics step."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.collision.rigidbody_collision import CollisionRigidBody2D

if TYPE_CHECKING:
    from core.packages.collision.collision_manager import CollisionManager
    from core.packages.collision.collision_resolver import CollisionResolver
    from core.packages.physics.rigidbody_2d import RigidBody2D


class PhysicsManager:
    """Physics manager runs the physics step."""

    def __init__(
        self,
        collision_manager: CollisionManager,
        collision_resolver: CollisionResolver,
        max_physics_steps: int = 5,
        collision_iterations: int = 10,
    ) -> None:
        """Initialize the PhysicsManager."""
        self.collision_manager = collision_manager
        self.collision_resolver = collision_resolver
        self.max_physics_steps = max_physics_steps
        self.collision_iterations = collision_iterations

    def run_physics_step(self, rigid_bodies: list[RigidBody2D], dt: float) -> None:
        """Run a single physics step."""
        for rb in rigid_bodies:
            rb.integrate_forces(dt)

        collisions = self.collision_manager.detect_collisions()

        rigid_body_collisions = [collision for collision in collisions if isinstance(collision, CollisionRigidBody2D)]

        for _ in range(self.collision_iterations):
            for collision in rigid_body_collisions:
                self.collision_resolver.solve_collision(collision)

        for collision in rigid_body_collisions:
            self.collision_resolver.correct_positions(collision)

        for rb in rigid_bodies:
            rb.integrate_velocity(dt)

        self.collision_manager.dispatch_events(collisions)
