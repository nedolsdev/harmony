"""A Tile is a cell of a TileMap."""

import pygame

from core.assets.surface_asset import SurfaceAsset
from game.material import Material
from game.vector2 import Vector2


class Tile(SurfaceAsset):
    """A Tile is a cell of a TileMap."""

    def __init__(self, tile_surface: SurfaceAsset, material: Material | None) -> None:
        """Initialize the Tile with a sprite image."""
        self.tile_surface = tile_surface
        self.material = material

    def get_surface(self) -> pygame.Surface:
        """Get the tile surface to render."""
        surface = self.tile_surface.get_surface().copy()
        if self.material:
            self.material.apply(surface)
        return surface

    def get_tile_surface_for_size(self, size: Vector2) -> pygame.Surface:
        """Get the tile surface for a given size."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)
