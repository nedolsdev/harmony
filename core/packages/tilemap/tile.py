"""A Tile is a cell of a TileMap."""

import pygame

from core.assets.surface_asset import ScalableSurfaceAsset
from core.packages.geometry.vector2 import Vector2
from game.material import Material


class Tile(ScalableSurfaceAsset):
    """A Tile is a cell of a TileMap."""

    def __init__(self, tile_surface: ScalableSurfaceAsset, material: Material | None) -> None:
        """Initialize the Tile with a sprite image."""
        self.tile_surface = tile_surface
        self.material = material

    def get_surface_of_scale(self, scale: Vector2) -> pygame.Surface:
        """Get the tile surface to render."""
        surface = self.tile_surface.get_surface_of_scale(scale).copy()
        if self.material:
            self.material.apply(surface)
        return surface
