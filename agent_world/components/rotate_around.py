"""A test behavior for rotating around a given point."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from core.components.transform import Transform
from game.behavior import Behavior
from game.vector2 import Vector2

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class RotateAround(Behavior):
    """A test behavior for rotating around a given point."""

    transform: Transform

    def __init__(self, point: Vector2, angular_speed: float, radius: float) -> None:
        """Initialize the movement behavior with an agent and speed. Angular speed is in degrees per frame."""
        super().__init__()
        self.point = point

        self.angular_speed = angular_speed

        self.current_angle = 0.0

        self.radius = radius

    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.transform = self.game_object.get_component(Transform)

    def start(self) -> None:
        """Initialize the rotate around behavior."""

    def update(self) -> None:
        """Update the rotate around behavior."""
        # update current angle
        self.current_angle += self.angular_speed
        self.current_angle %= 360

        # calculate new position
        radius = self.radius
        rad_angle = math.radians(self.current_angle)
        new_x = self.point.x + radius * math.cos(rad_angle)
        new_y = self.point.y + radius * math.sin(rad_angle)

        self.transform.world_position = Vector2(new_x, new_y)

        # update rotation to face the direction of movement
        self.transform.local_rotation = rad_angle + math.pi / 2

    def add_events(self, event_handler: EventHandler) -> None:
        """Register rotate event listeners with the event handler."""

    def copy(self) -> RotateAround:
        """Create a copy of the rotate around behavior."""
        new_rotate_around = RotateAround(self.point, self.angular_speed, self.radius)
        new_rotate_around.transform = self.transform.copy()
        return new_rotate_around
