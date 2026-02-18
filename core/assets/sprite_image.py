"""A SpriteImage Asset."""

import pygame

from game.asset import Asset
from game.image_cache import ImageCache


class SpriteImage(Asset):
    """A SpriteImage Asset."""

    def __init__(self, image_path: str) -> None:
        """Initialize the sprite image with a file path."""
        self.image_path = image_path

    def load(self) -> pygame.Surface:
        """Lazily load and return the image surface."""
        return ImageCache.load(self.image_path)
