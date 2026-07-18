"""A test behavior for rotating around a given point."""

from __future__ import annotations

import math

from harmony.core.components.transform import Transform
from harmony.game.behavior import Behavior


class RotateAround(Behavior):
    """A test behavior for rotating around a given point."""

    transform: Transform

    def __init__(self, angular_speed: float) -> None:
        """Initialize the movement behavior with an agent and speed. Angular speed is in degrees per frame."""
        super().__init__()

        self.angular_speed = angular_speed

        self.current_angle = 0.0

    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.transform = self.game_object.get_component(Transform)

    def update(self) -> None:
        """Update the rotate around behavior."""
        self.transform.local_rotation += math.radians(self.angular_speed)

    def copy(self) -> RotateAround:
        """Create a copy of the rotate around behavior."""
        new_rotate_around = RotateAround(self.angular_speed)
        new_rotate_around.transform = self.transform.copy()
        return new_rotate_around
