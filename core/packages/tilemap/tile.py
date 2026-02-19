"""A Tile is a cell of a TileMap."""

import pygame

from core.assets.surface_asset import SurfaceAsset
from game.material import Material


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
