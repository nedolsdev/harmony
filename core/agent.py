"""The agent module defines the agent's behavior and interactions with the game state."""


class Agent:
    """Represents an agent in the game."""

    def __init__(self, position: tuple[int, int]) -> None:
        """Initialize the agent with a position."""
        self.position = position

    def move_up(self) -> None:
        """Move the agent up."""
        x, y = self.position
        self.position = (x, y - 1)

    def move_down(self) -> None:
        """Move the agent down."""
        x, y = self.position
        self.position = (x, y + 1)

    def move_left(self) -> None:
        """Move the agent left."""
        x, y = self.position
        self.position = (x - 1, y)

    def move_right(self) -> None:
        """Move the agent right."""
        x, y = self.position
        self.position = (x + 1, y)

    def get_position(self) -> tuple[int, int]:
        """Return the agent's current position."""
        return self.position
