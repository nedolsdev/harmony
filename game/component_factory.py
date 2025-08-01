"""The component factory module defines the ComponentFactory class for creating game components."""

from core.components.position import Position
from core.components.sprite_2d import Sprite2D, SpriteImage
from game.material import Material


class ComponentFactory:
    """A static factory class for creating the base engine game components."""

    @staticmethod
    def position(x: int, y: int) -> Position:
        """Create a position component."""
        return Position(x, y)

    @staticmethod
    def sprite_2d(width: int, height: int, material: Material, image: SpriteImage | None = None) -> Sprite2D:
        """Create a 2D sprite component."""
        return Sprite2D(width, height, material, image)
