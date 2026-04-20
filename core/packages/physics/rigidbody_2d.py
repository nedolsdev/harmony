"""RigidBody2D component."""

from __future__ import annotations

import math
from typing import override

from core.components.transform import Transform
from core.packages.geometry.vector2 import Vector2
from core.packages.timing.delta_time import DeltaTime
from game.behavior import Behavior


class RigidBody2D(Behavior):
    """RigidBody2D component."""

    EPSILON = 1e-5

    def __init__(  # noqa: PLR0913
        self,
        *,
        mass: float | None = None,
        velocity: Vector2 | None = None,
        angular_velocity: float | None = None,
        angular_damping: float | None = None,
        linear_damping: float | None = None,
        center_of_mass: Vector2 | None = None,
        moment_of_inertia: float | None = None,
    ) -> None:
        """RigidBody2D component."""
        super().__init__(disallow_multiple_of_type=True, disallow_multiple_of_exact_type=True)
        self._mass: float = 0.0
        self.inverse_mass: float = 0.0

        self._moment_of_inertia: float = 0.0
        self.inverse_inertia: float = 0.0

        self.mass = mass or 1
        self.moment_of_inertia = moment_of_inertia or 0.0

        self.velocity: Vector2 = velocity or Vector2.zero()
        self.acceleration: Vector2 = Vector2.zero()
        self.angular_velocity: float = angular_velocity or 0
        self.angular_damping: float = angular_damping or 0
        self.linear_damping: float = linear_damping or 0
        self.center_of_mass: Vector2 = center_of_mass or Vector2.zero()

        self.force: Vector2 = Vector2.zero()
        self.torque: float = 0.0

    @property
    def mass(self) -> float:
        """Mass of the RigidBody."""
        return self._mass

    @mass.setter
    def mass(self, value: float) -> None:
        self._mass = value
        self.inverse_mass = 1.0 / value if value > 0.0 else 0.0

        if value == 0.0:
            self.velocity = Vector2.zero()
            self.angular_velocity = 0.0

    @property
    def moment_of_inertia(self) -> float:
        """Moment of inertia of the RigidBody."""
        return self._moment_of_inertia

    @moment_of_inertia.setter
    def moment_of_inertia(self, value: float) -> None:
        self._moment_of_inertia = value
        self.inverse_inertia = 1.0 / value if value > 0.0 else 0.0

        if value == 0.0:
            self.angular_velocity = 0.0

    @override
    def fixed_update(self) -> None:
        """Advance the rigid body by dt seconds using semi-implicit Euler."""
        # TODO: Fix with explicit dependency  # noqa: TD003
        if not self.game_object.has_component(Transform):
            msg = "A GameObject with RigidBody2D requires a Transform."
            raise ValueError(msg)

        # sync from transform
        transform = self.game_object.get_component(Transform)
        position = transform.world_position
        rotation = transform.world_rotation

        dt = DeltaTime.get_delta_time()

        self.acceleration = self.force * self.inverse_mass
        self.velocity += self.acceleration * dt

        if self.linear_damping > 0.0:
            self.velocity *= math.exp(-self.linear_damping * dt)

        # stop micro movement
        if self.velocity.magnitude_squared() < self.EPSILON:
            self.velocity = Vector2.zero()

        position += self.velocity * dt

        angular_acceleration = self.torque * self.inverse_inertia
        self.angular_velocity += angular_acceleration * dt

        if self.angular_damping > 0.0:
            self.angular_velocity *= math.exp(-self.angular_damping * dt)

        # stop micro rotations
        if abs(self.angular_velocity) < self.EPSILON:
            self.angular_velocity = 0.0

        rotation += self.angular_velocity * dt

        # resync transform
        transform.world_position = position
        transform.world_rotation = rotation

        self.force = Vector2.zero()
        self.torque = 0.0

    def apply_force(self, force: Vector2) -> None:
        """Apply force at center of mass."""
        self.force += force

    def apply_force_at_point(self, force: Vector2, point: Vector2) -> None:
        """Apply force at world-space point."""
        self.force += force

        if not self.game_object.has_component(Transform):
            msg = "A GameObject with RigidBody2D requires a Transform."
            raise ValueError(msg)

        transform = self.game_object.get_component(Transform)
        position = transform.world_position

        offset: Vector2 = point - (position + self.center_of_mass)
        self.torque += offset.x * force.y - offset.y * force.x

    def apply_torque(self, torque: float) -> None:
        """Apply pure torque."""
        self.torque += torque

    def apply_linear_impulse(self, impulse: Vector2) -> None:
        """Apply instantaneous linear impulse."""
        self.velocity += impulse * self.inverse_mass

    def apply_angular_impulse(self, impulse: float) -> None:
        """Apply instantaneous angular impulse."""
        self.angular_velocity += impulse * self.inverse_inertia
