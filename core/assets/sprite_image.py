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

    @staticmethod
    def get_default_sprite_surface(size: tuple[int, int]) -> pygame.Surface:
        """Return a default sprite surface with the given size."""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 255, 255, 255))
        return surface
