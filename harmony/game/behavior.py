"""The behavior module defines a game object interacts with the game state."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.game.component import GameComponent

if TYPE_CHECKING:
    from harmony.game.event_handler import EventHandler
    from harmony.game.object import GameObject


class Behavior(GameComponent):
    """A behavior is a special type of game component that defines how a game object interacts with the game state."""

    game_object: GameObject

    def set_owner(self, owner: GameObject) -> None:
        """Set the owner of the behavior."""
        self.game_object = owner

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
    def late_update(self) -> None:
        """Late update the component every frame."""

    @override
    def fixed_update(self) -> None:
        """Update the component in the physics / fixed loop."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
