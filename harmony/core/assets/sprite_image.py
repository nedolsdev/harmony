"""A SpriteImage Asset."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from harmony.core.assets.surface_asset import ScalableSurfaceAsset
from harmony.core.packages.render.resolution import ResolutionManager
from harmony.game.image_cache import ImageCache

if TYPE_CHECKING:
    from harmony.core.packages.geometry.vector2 import Vector2


class SpriteImage(ScalableSurfaceAsset):
    """A SpriteImage Asset."""

    def __init__(self, image_path: str) -> None:
        """Initialize the sprite image with a file path."""
        self.image_path = image_path
        super().__init__()

    def get_surface(self) -> pygame.Surface:
        """Lazily load and return the image surface."""
        return ImageCache.load(self.image_path)

    @staticmethod
    def get_default_sprite_surface(size: tuple[float, float]) -> pygame.Surface:
        """Return a default sprite surface with the given size."""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 255, 255, 255))
        return surface

    def get_size(self) -> tuple[int, int]:
        """Get the size of the sprite image."""
        surface = self.get_surface()
        return surface.get_size()

    @override
    def get_surface_of_scale(self, scale: Vector2, *, use_smooth_scaling: bool = False) -> pygame.Surface:
        return ResolutionManager.scale_surface(self.get_surface(), scale, use_smooth_scaling=use_smooth_scaling)


class SlicedSpriteImage(SpriteImage):
    """A SpriteImage Asset loaded from a portion of a larger asset source."""

    def __init__(self, image_path: str, x: int, y: int, width: int, height: int) -> None:
        """Initialize the sprite image with a file path."""
        super().__init__(image_path)
        self._rect = (x, y, width, height)

    def get_surface(self) -> pygame.Surface:
        """Lazily load and return the image surface."""
        source: pygame.Surface = ImageCache.load(self.image_path)
        return source.subsurface(self._rect).copy()
