"""The rotation module defines a component that holds the rotation of a game object."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from game.component import GameComponent

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class Rotation(GameComponent):
    """A component that holds the rotation of a game object."""

    _rotation: float
    """The rotation value stored in radians."""

    def __init__(self, *, degrees: float | None = None, radians: float | None = None) -> None:
        """Initialize the position component with x and y coordinates."""
        super().__init__(disallow_multiple_of_type=True)
        self.set_rotation(degrees=degrees, radians=radians)

    def set_rotation(self, *, degrees: float | None = None, radians: float | None = None) -> None:
        """Set the rotation of the object."""
        # can't provide both degrees and radians
        if degrees is not None and radians is not None:
            msg = "Only provide 'degrees' or 'radians' as an argument to rotation, not both."
            raise ValueError(msg)
        if degrees is not None:
            self._rotation = self._convert_degrees_to_radians(degrees)
        elif radians is not None:
            self._rotation = self._normalize_radian(radians)

    @staticmethod
    def _normalize_degree(deg: float) -> float:
        """Normalize any degree value (including negatives) to a value between 0 and 359."""
        return deg % 360

    @staticmethod
    def _normalize_radian(rad: float) -> float:
        """Normalize any radian value (including negatives) to a value between 0 and math.pi * 2 - epsilon."""
        return rad % (math.pi * 2)

    @staticmethod
    def _convert_degrees_to_radians(deg: float) -> float:
        """Convert any degree value to radian."""
        deg = Rotation._normalize_degree(deg)
        return deg * math.pi / 180

    @staticmethod
    def _convert_radians_to_degrees(rad: float) -> float:
        """Convert any radian value to degree."""
        rad = Rotation._normalize_radian(rad)
        return rad * 180 / math.pi

    def get_degrees(self) -> float:
        """Get the rotation of the object in degrees."""
        return self._convert_radians_to_degrees(self._rotation)

    def get_radians(self) -> float:
        """Get the rotation of the object in radians."""
        return self._rotation

    def get_rotation(self) -> float:
        """Get the rotation of the object in radians. Same as 'get_radians'."""
        return self.get_radians()

    def awake(self) -> None:
        """Event call when the script instance is created."""

    def start(self) -> None:
        """Initialize the position component."""

    def update(self) -> None:
        """Update the position component."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def copy(self) -> Rotation:
        """Create a copy of the position component."""
        return Rotation(radians=self._rotation)
