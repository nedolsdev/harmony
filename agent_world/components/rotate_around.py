"""A test behavior for rotating around a given point."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from core.components.position import Position
from core.components.rotation import Rotation
from game.behavior import Behavior

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class RotateAround(Behavior):
    """A test behavior for rotating around a given point."""

    position: Position
    rotation: Rotation

    def __init__(self, point: Position, angular_speed: float, radius: float) -> None:
        """Initialize the movement behavior with an agent and speed. Angular speed is in degrees per frame."""
        super().__init__()
        self.point = point

        self.angular_speed = angular_speed

        self.current_angle = 0.0

        self.radius = radius

    def get_position(self) -> tuple[int, int]:
        """Return the agent's current position."""
        return self.position.get_coordinates()

    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.position = self.game_object.get_component(Position)
        self.rotation = self.game_object.get_component(Rotation)

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

        self.position.set_coordinates(int(new_x), int(new_y))

        # update rotation to face the direction of movement
        if self.rotation:
            self.rotation.set_rotation(radians=rad_angle + math.pi / 2)

    def add_events(self, event_handler: EventHandler) -> None:
        """Register rotate event listeners with the event handler."""

    def copy(self) -> RotateAround:
        """Create a copy of the rotate around behavior."""
        new_rotate_around = RotateAround(self.point, self.angular_speed, self.radius)
        if self.position and self.rotation:
            new_rotate_around.position = self.position.copy()
            new_rotate_around.rotation = self.rotation.copy()
        return new_rotate_around
