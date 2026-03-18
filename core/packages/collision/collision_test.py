"""Collision test component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from game.behavior import Behavior

if TYPE_CHECKING:
    from core.packages.collision.collision import Collision
    from game.event_handler import EventHandler


class CollisionTest(Behavior):
    """A component that uses a timer."""

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def copy(self) -> CollisionTest:
        """Create a copy of the timer component."""
        return self

    @override
    def on_collision_enter(self, collision: Collision) -> None:
        print("Collision enter!")  # noqa: T201

    @override
    def on_collision_stay(self, collision: Collision) -> None:
        print("Collision stay!")  # noqa: T201

    @override
    def on_collision_exit(self, collision: Collision) -> None:
        print("Collision exit!")  # noqa: T201
