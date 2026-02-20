"""The position module defines a component that holds the position of a game object."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.animation.animatable import Animatable
from core.packages.animation.frame import VectorFrame
from game.component import GameComponent
from game.local import Local
from game.vector2 import Vector2

if TYPE_CHECKING:
    from game.event_handler import EventHandler

PositionFrame = VectorFrame[tuple[float, float, float]]


class Position(GameComponent, Animatable[PositionFrame], Local["Position"]):
    """A component that holds the position of a game object."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize the position component with x and y coordinates."""
        super().__init__(disallow_multiple_of_type=True)
        self.vector = Vector2(x, y)

    @override
    def awake_local(self) -> None:
        self.local = Position(0, 0)

    def get_coordinates(self) -> tuple[float, float]:
        """Return the x and y coordinates of the position."""
        if not self.has_local():
            return self.vector.as_tuple()

        return (self.local.vector + self.vector).as_tuple()

    def set_coordinates(self, x: float, y: float) -> None:
        """Set the x and y coordinates of the position."""
        self.vector = Vector2(x, y)

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
        pos = Position(self.vector.x, self.vector.y)

        if pos.has_local():
            pos.local = self.local.copy()

        return pos

    @override
    def set_animation_frame(self, frame: PositionFrame, *, target_local_if_available: bool) -> None:
        """Set or update the component based on the frame."""
        if target_local_if_available:
            self.local.set_coordinates(frame.vector[0], frame.vector[1])
        else:
            self.set_coordinates(frame.vector[0], frame.vector[1])

    def get_vector(self) -> Vector2:
        """Get the true position (local + global)."""
        if self.local.vector is None:
            return self.vector
        return self.vector + self.local.vector
