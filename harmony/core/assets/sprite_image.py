"""A SpriteImage Asset."""

from __future__ import annotations

from harmony.core.packages.geometry.vector2 import Vector2
from harmony.game.asset import Asset


class SpriteImage(Asset):
    """A SpriteImage Asset."""

    def __init__(self, image_path: str, true_pixel_size: Vector2, scale: Vector2 | None = None) -> None:
        """Initialize the sprite image with a file path."""
        super().__init__()
        self.image_path = image_path
        self.true_pixel_size = true_pixel_size
        self.scale = scale or Vector2.one()


class SlicedSpriteImage(SpriteImage):
    """A SpriteImage Asset loaded from a portion of a larger asset source."""

    def __init__(self, image_path: str, x: int, y: int, width: int, height: int) -> None:
        """Initialize the sprite image with a file path."""
        super().__init__(image_path, Vector2(width, height))
        self.position = (x, y)
