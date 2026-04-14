"""The base geometry primitive."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class Geometry:
    """The base geometry primitive."""

    def copy(self) -> Self:
        """Create a copy of the geometry."""
        msg = f"'{self.__class__.__name__}' does not implement 'copy' method."
        raise NotImplementedError(msg)

    def bounds(self) -> tuple[float, float, float, float]:
        """Get the rectangular bounds of the geometry (min_x, max_x, min_y, max_y)."""
        msg = f"'{self.__class__.__name__}' does not implement 'bounds' method."
        raise NotImplementedError(msg)


class ScalableVector1:
    """A geometry that is scalable by a constant."""

    def scale(self, factor: float) -> Self:
        """Create a new geometry from a given scale."""
        msg = f"'{self.__class__.__name__}' does not implement 'scale' method."
        raise NotImplementedError(msg)


class ScalableVector2:
    """A geometry that is scalable by a Vector2."""

    def scale(self, factor: Vector2) -> Self:
        """Create a new geometry from a given scale."""
        msg = f"'{self.__class__.__name__}' does not implement 'scale' method."
        raise NotImplementedError(msg)


class Rotatable:
    """A geometry that is rotatable."""

    def rotate_radians(self, radians: float) -> Self:
        """Create a new geometry from a given rotation in radians."""
        msg = f"'{self.__class__.__name__}' does not implement 'rotate' method."
        raise NotImplementedError(msg)

    def rotate_degrees(self, degrees: float) -> Self:
        """Create a new geometry from a given rotation in degrees."""
        return self.rotate_radians(math.radians(degrees))
