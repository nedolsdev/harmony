"""The base geometry primitive."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from harmony.core.packages.geometry.vector2 import Vector2


class Geometry(ABC):
    """The base geometry primitive."""

    @abstractmethod
    def copy(self) -> Self:
        """Create a copy of the geometry."""

    @abstractmethod
    def bounds(self) -> tuple[float, float, float, float]:
        """Get the rectangular bounds of the geometry (min_x, max_x, min_y, max_y)."""

    def size(self) -> tuple[float, float]:
        """Get the size of the bounds of the geometry (x, y)."""
        min_x, max_x, min_y, max_y = self.bounds()
        return max_x - min_x, max_y - min_y

    def top_left(self) -> tuple[float, float]:
        """Get the top-left corner of the geometry bounds (x, y)."""
        min_x, _, min_y, _ = self.bounds()
        return min_x, min_y


class ScalableVector1(ABC):
    """A geometry that is scalable by a constant."""

    @abstractmethod
    def scale(self, factor: float) -> Self:
        """Create a new geometry from a given scale."""


class ScalableVector2(ABC):
    """A geometry that is scalable by a Vector2."""

    @abstractmethod
    def scale(self, factor: Vector2) -> Self:
        """Create a new geometry from a given scale."""


class Rotatable(ABC):
    """A geometry that is rotatable."""

    @abstractmethod
    def rotate_radians(self, radians: float) -> Self:
        """Create a new geometry from a given rotation in radians."""

    def rotate_degrees(self, degrees: float) -> Self:
        """Create a new geometry from a given rotation in degrees."""
        return self.rotate_radians(math.radians(degrees))
