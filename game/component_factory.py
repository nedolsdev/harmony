"""The component factory module defines the ComponentFactory class for creating game components."""

from core.components.mesh_2d import Material, Mesh2D
from core.components.position import Position


class ComponentFactory:
    """A static factory class for creating the base engine game components."""

    @staticmethod
    def position(x: int, y: int) -> Position:
        """Create a position component."""
        return Position(x, y)

    @staticmethod
    def mesh_2d(width: int, height: int, material: Material) -> Mesh2D:
        """Create a 2D mesh component."""
        return Mesh2D(width, height, material)
