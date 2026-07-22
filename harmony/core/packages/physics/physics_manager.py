"""Physics manager runs the physics step."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from harmony.core.packages.collision.rigidbody_collision import CollisionRigidBody2D
from harmony.core.packages.physics.rigidbody_2d import RigidBody2D
from harmony.core.packages.timing.delta_time import DeltaTime
from harmony.game.system import System

if TYPE_CHECKING:
    from harmony.core.packages.collision.collision_manager import CollisionManager
    from harmony.core.packages.collision.collision_resolver import CollisionResolver
    from harmony.game.system_manager import SystemManager


@dataclass(slots=True)
class PhysicsSettings:
    """Physics system settings."""

    max_physics_steps: int = 5
    collision_iterations: int = 10
    physics_tps: int = 60


class PhysicsSystem(System):
    """Physics manager runs the physics step."""

    def __init__(
        self,
        collision_manager: CollisionManager,
        collision_resolver: CollisionResolver,
        system_manager: SystemManager,
        settings: PhysicsSettings | None = None,
    ) -> None:
        """Initialize the PhysicsManager."""
        super().__init__()
        self.collision_manager = collision_manager
        self.collision_resolver = collision_resolver
        self.settings = settings or PhysicsSettings()
        self.physics_fixed_dt: float = 1.0 / self.settings.physics_tps
        self.physics_accumulator: float = 0.0

        self.system_manager = system_manager

        self.rigid_bodies = self._add_channel(RigidBody2D, system_manager.component_manager)

    def run_physics_step(self, rigid_bodies: set[RigidBody2D], dt: float) -> None:
        """Run a single physics step."""
        for rb in rigid_bodies:
            rb.integrate_forces(dt)

        collisions = self.collision_manager.detect_collisions()

        rigid_body_collisions = [collision for collision in collisions if isinstance(collision, CollisionRigidBody2D)]

        for _ in range(self.settings.collision_iterations):
            for collision in rigid_body_collisions:
                self.collision_resolver.solve_collision(collision)

        for collision in rigid_body_collisions:
            self.collision_resolver.correct_positions(collision)

        for rb in rigid_bodies:
            rb.integrate_velocity(dt)

        self.collision_manager.dispatch_events(collisions)

    def pre_update(self) -> None:
        """Update the physics."""
        frame_dt = DeltaTime.get_unscaled_delta_time()
        self.physics_accumulator += frame_dt

        rigid_bodies: set[RigidBody2D] = set()

        # only filter when needed for performance
        if self.physics_accumulator >= self.physics_fixed_dt:
            rigid_bodies = self.rigid_bodies.get_components()

        # fixed step physics loop
        steps: int = 0

        while self.physics_accumulator >= self.physics_fixed_dt:
            self.run_physics_step(rigid_bodies, self.physics_fixed_dt)

            self.system_manager.fixed_update()

            self.physics_accumulator -= self.physics_fixed_dt
            steps += 1

            if steps >= self.settings.max_physics_steps:
                self.physics_accumulator = 0.0
                break
