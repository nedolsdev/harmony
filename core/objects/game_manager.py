"""The game manager module contains the game object that manages the game state."""

from game.object import GameObject


class GameManager(GameObject):
    """Manages the game state and interactions between game objects."""

    def __init__(self) -> None:
        """Initialize the game manager."""
        super().__init__()
        self.tags.add("game_manager")
