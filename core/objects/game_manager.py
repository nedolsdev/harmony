"""The game manager module contains the game object that manages the game state."""

from game.event_handler import EventHandler
from game.object import GameObject


class GameManager(GameObject):
    """Manages the game state and interactions between game objects."""

    def __init__(self, event_handler: EventHandler) -> None:
        """Initialize the game manager."""
        super().__init__(event_handler)
        self.tags.add("game_manager")
