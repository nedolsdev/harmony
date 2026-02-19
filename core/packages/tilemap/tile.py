"""A Tile is a cell of a TileMap."""

import pygame

from core.assets.sprite_image import SpriteImage
from game.material import Material


class Tile:
    """A Tile is a cell of a TileMap."""

    def __init__(self, sprite: SpriteImage | None, material: Material) -> None:
        """Initialize the Tile with a sprite image."""
        self.sprite = sprite
        self.material = material
