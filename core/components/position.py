"""The position module defines a component that holds the position of a game object."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.animation.animatable import Animatable
from core.packages.animation.frame import VectorFrame
from game.component import GameComponent
from game.local import Local

if TYPE_CHECKING:
    from game.event_handler import EventHandler

PositionFrame = VectorFrame[tuple[int, int, int]]


class Position(GameComponent, Animatable[PositionFrame], Local["Position"]):
    """A component that holds the position of a game object."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the position component with x and y coordinates."""
        super().__init__(disallow_multiple_of_type=True)
        self.x = x
        self.y = y

    @override
    def awake_local(self) -> None:
        self.local = Position(0, 0)

    def get_coordinates(self) -> tuple[int, int]:
        """Return the x and y coordinates of the position."""
        # sometimes we might not have local because we are just using this for points
        # it's a bit hacky, but it is what it is
        if not self.has_local():
            return self.x, self.y

        return self.x + self.local.x, self.y + self.local.y

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
        pos = Position(self.x, self.y)

        if pos.has_local():
            pos.local = self.local.copy()

        return pos

    def __sub__(self, other: Position) -> Position:
        """Subtract two Position objects."""
        pos = self.copy()
        pos.set_coordinates(self.x - other.x, self.y - other.y)
        return pos

    def __add__(self, other: Position) -> Position:
        """Add two Position objects."""
        pos = self.copy()
        pos.set_coordinates(self.x + other.x, self.y + other.y)
        return pos

    @override
    def set_animation_frame(self, frame: PositionFrame, *, target_local_if_available: bool) -> None:
        """Set or update the component based on the frame."""
        if target_local_if_available:
            self.local.set_coordinates(frame.vector[0], frame.vector[1])
        else:
            self.set_coordinates(frame.vector[0], frame.vector[1])
