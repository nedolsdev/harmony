"""The behavior module defines a game object interacts with the game state."""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.component import GameComponent

if TYPE_CHECKING:
    from game.object import GameObject


class Behavior(GameComponent):
    """A behavior is a special type of game component that defines how a game object interacts with the game state."""

    game_object: GameObject

    def set_owner(self, owner: GameObject) -> None:
        """Set the owner of the behavior."""
        self.game_object = owner
