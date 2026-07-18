"""Simple camera controller for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from harmony.core.components.transform import Transform
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.game.behavior import Behavior
from harmony.game.event import PygameKeyStateEvent

if TYPE_CHECKING:
    from collections.abc import Callable

    from harmony.game.event_handler import EventHandler


class CameraController(Behavior):
    """Simple camera controller for testing."""

    def __init__(self, speed: int = 50) -> None:
        """Initialize the CameraController."""
        super().__init__()
        self.speed = speed

    transform: Transform

    def move(self, vector: Vector2) -> Callable[[], None]:
        """Move in a direction."""

        def inner() -> None:
            self.transform.local_position += vector

        return inner

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.transform = self.game_object.get_component(Transform)

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
        event_handler.register_listener(
            PygameKeyStateEvent.get_name_from_key(pygame.K_UP, event_type=pygame.KEYDOWN),
            self.move(Vector2(0, -self.speed)),
        )
        event_handler.register_listener(
            PygameKeyStateEvent.get_name_from_key(pygame.K_DOWN, event_type=pygame.KEYDOWN),
            self.move(Vector2(0, self.speed)),
        )
        event_handler.register_listener(
            PygameKeyStateEvent.get_name_from_key(pygame.K_LEFT, event_type=pygame.KEYDOWN),
            self.move(Vector2(-self.speed, 0)),
        )
        event_handler.register_listener(
            PygameKeyStateEvent.get_name_from_key(pygame.K_RIGHT, event_type=pygame.KEYDOWN),
            self.move(Vector2(self.speed, 0)),
        )

    def copy(self) -> CameraController:
        """Create a copy of the movement behavior."""
        return CameraController()
