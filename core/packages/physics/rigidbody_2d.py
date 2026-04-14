"""RigidBody2D component."""

from __future__ import annotations

from core.packages.geometry.vector2 import Vector2


class RigidBody2D:
    """RigidBody2D component."""

    def __init__(  # noqa: PLR0913
        self,
        *,
        mass: float | None = None,
        position: Vector2 | None = None,
        rotation: float | None = None,
        velocity: Vector2 | None = None,
        acceleration: Vector2 | None = None,
        angular_velocity: float | None = None,
        # how fast angular velocity decreases
        angular_damping: float | None = None,
        center_of_mass: Vector2 | None = None,
    ) -> None:
        """RigidBody2D component."""
        self.mass: float = mass or 0
        self.position: Vector2 = position or Vector2.zero()
        self.rotation: float = rotation or 0
        self.velocity: Vector2 = velocity or Vector2.zero()
        self.acceleration: Vector2 = acceleration or Vector2.zero()
        self.angular_velocity: float = angular_velocity or 0
        self.angular_damping: float = angular_damping or 0
        self.center_of_mass: Vector2 = center_of_mass or Vector2.zero()
