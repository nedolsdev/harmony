"""The agent module defines the agent's behavior and interactions with the game state."""

from game.object import GameObject


class Agent(GameObject):
    """Represents an agent in the game."""

    def __init__(self, position: tuple[int, int], width: int, height: int) -> None:
        """Initialize the agent with a position."""
        super().__init__(position, width, height)
        self.tags.add("agent")

    def move_up(self) -> None:
        """Move the agent up by one tile."""
        x, y = self.position.get_coordinates()
        self.position.set_coordinates(x, y - 1)

    def move_down(self) -> None:
        """Move the agent down by one tile."""
        x, y = self.position.get_coordinates()
        self.position.set_coordinates(x, y + 1)

    def move_left(self) -> None:
        """Move the agent left by one tile."""
        x, y = self.position.get_coordinates()
        self.position.set_coordinates(x - 1, y)

    def move_right(self) -> None:
        """Move the agent right by one tile."""
        x, y = self.position.get_coordinates()
        self.position.set_coordinates(x + 1, y)

    def get_position(self) -> tuple[int, int]:
        """Return the agent's current position."""
        return self.position.get_coordinates()
