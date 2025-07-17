"""The state module defines the game state, including the grid and the agent's position."""

from core.agent import Agent
from world.grid import GridGenerator


class GameState:
    """Represents the current state of the game."""

    def __init__(self) -> None:
        """Initialize the game state with a grid."""
        self.grid = GridGenerator.generate()
        self.agent = Agent((0, 0))
        self.game_quit = False
