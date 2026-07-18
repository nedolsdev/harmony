"""A Tile is a cell of a TileMap."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.assets.surface_asset import ScalableSurfaceAsset

if TYPE_CHECKING:
    import pygame

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
