"""The state module defines the game state, including the grid and the agent's position."""

from game.object import GameObject
from world.grid import GridGenerator


class GameState:
    """Represents the current state of the game."""

    def __init__(self) -> None:
        """Initialize the game state with a grid."""
        self.grid = GridGenerator.generate()
        self.game_objects: list[GameObject] = []

    def add_game_object(self, game_object: GameObject) -> None:
        """Add a game object to the game state."""
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject) -> None:
        """Remove a game object from the game state."""
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)

    def get_game_objects(self) -> list[GameObject]:
        """Return the list of game objects in the game state."""
        return self.game_objects

    def find_with_tag(self, tag: str) -> list[GameObject]:
        """Find all game objects with a specific tag."""
        return [obj for obj in self.game_objects if tag in obj.tags]
