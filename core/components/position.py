"""The position module defines a component that holds the position of a game object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.component import GameComponent

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class Position(GameComponent):
    """A component that holds the position of a game object."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the position component with x and y coordinates."""
        super().__init__(disallow_multiple_of_type=True)
        self.x = x
        self.y = y

    def get_coordinates(self) -> tuple[int, int]:
        """Return the x and y coordinates of the position."""
        return self.x, self.y

    def set_coordinates(self, x: int, y: int) -> None:
        """Set the x and y coordinates of the position."""
        self.x = x
        self.y = y

    def awake(self) -> None:
        """Event call when the script instance is created."""

    def start(self) -> None:
        """Initialize the position component."""

    def update(self) -> None:
        """Update the position component."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def copy(self) -> Position:
        """Create a copy of the position component."""
        return Position(self.x, self.y)
