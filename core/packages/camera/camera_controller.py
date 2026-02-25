"""Simple camera controller for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.components.transform import Transform
from game.behavior import Behavior
from game.event import PygameKeydownEvent
from game.vector2 import Vector2

if TYPE_CHECKING:
    from collections.abc import Callable

    from game.event_handler import EventHandler


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
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
        event_handler.register_listener(
            PygameKeydownEvent.get_name_from_key(pygame.K_UP),
            self.move(Vector2(0, -self.speed)),
        )
        event_handler.register_listener(
            PygameKeydownEvent.get_name_from_key(pygame.K_DOWN),
            self.move(Vector2(0, self.speed)),
        )
        event_handler.register_listener(
            PygameKeydownEvent.get_name_from_key(pygame.K_LEFT),
            self.move(Vector2(-self.speed, 0)),
        )
        event_handler.register_listener(
            PygameKeydownEvent.get_name_from_key(pygame.K_RIGHT),
            self.move(Vector2(self.speed, 0)),
        )

    def copy(self) -> CameraController:
        """Create a copy of the movement behavior."""
        return CameraController()
