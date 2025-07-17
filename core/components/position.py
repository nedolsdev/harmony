"""The position module defines a component that holds the position of a game object."""

from game.component import GameComponent
from game.event_handler import EventHandler


class Position(GameComponent):
    """A component that holds the position of a game object."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the position component with x and y coordinates."""
        super().__init__()
        self.x = x
        self.y = y

    def get_coordinates(self) -> tuple[int, int]:
        """Return the x and y coordinates of the position."""
        return self.x, self.y

    def set_coordinates(self, x: int, y: int) -> None:
        """Set the x and y coordinates of the position."""
        self.x = x
        self.y = y

    def start(self) -> None:
        """Initialize the position component."""

    def update(self) -> None:
        """Update the position component."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
