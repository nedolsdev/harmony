"""Physics manager runs the physics step."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.collision.rigidbody_collision import CollisionRigidBody2D
from harmony.core.packages.physics.rigidbody_2d import RigidBody2D

if TYPE_CHECKING:
    from harmony.core.packages.collision.collision_manager import CollisionManager
    from harmony.core.packages.collision.collision_resolver import CollisionResolver
    from harmony.game.object import GameObject


class PhysicsManager:
    """Physics manager runs the physics step."""

    def __init__(
        self,
        collision_manager: CollisionManager,
        collision_resolver: CollisionResolver,
        max_physics_steps: int = 5,
        collision_iterations: int = 10,
        physics_tps: int = 60,
    ) -> None:
        """Initialize the PhysicsManager."""
        self.collision_manager = collision_manager
        self.collision_resolver = collision_resolver
        self.max_physics_steps = max_physics_steps
        self.collision_iterations = collision_iterations

        self.physics_tps = physics_tps
        self.physics_fixed_dt: float = 1.0 / self.physics_tps
        self.physics_accumulator: float = 0.0

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

    def update(self, objects: list[GameObject], frame_dt: float) -> None:
        """Update the physics."""
        self.physics_accumulator += frame_dt

        rigid_bodies: list[RigidBody2D] = []

        # only filter when needed for performance
        if self.physics_accumulator >= self.physics_fixed_dt:
            rigid_bodies = [obj.get_component(RigidBody2D) for obj in objects if obj.has_component(RigidBody2D)]

        # fixed step physics loop
        steps: int = 0

        while self.physics_accumulator >= self.physics_fixed_dt:
            self.run_physics_step(rigid_bodies, self.physics_fixed_dt)

            for obj in objects:
                obj.fixed_update()

            self.physics_accumulator -= self.physics_fixed_dt
            steps += 1

            if steps >= self.max_physics_steps:
                self.physics_accumulator = 0.0
                break
