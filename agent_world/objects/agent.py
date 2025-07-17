"""The agent module defines the agent's behavior and interactions with the game state."""

from core.components.mesh_2d import Mesh2D
from core.components.position import Position
from game.object import GameObject


class Agent(GameObject):
    """Represents an agent in the game."""

    def __init__(self, position: tuple[int, int], width: int, height: int) -> None:
        """Initialize the agent with a position."""
        super().__init__()
        self.tags.add("agent")

        # add position component
        self.components.append(Position(*position))

        # add mesh component
        self.components.append(Mesh2D(width, height))

        # add mesh component to tags
        self.tags.add("mesh")
