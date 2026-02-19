"""The TileMapRenderer defines how the TileMap is drawn to the screen."""

from typing import override

import pygame

from core.assets.sprite_image import SpriteImage
from core.components.position import Position
from core.components.render import Render
from core.components.rotation import Rotation
from core.packages.tilemap.grid import Grid
from core.packages.tilemap.tile import Tile
from core.packages.tilemap.tile_map import TileMap
from game.vector2 import Vector2


class TileMapRenderer(Render):
    """The TileMapRenderer defines how the TileMap is drawn to the screen."""

    def __init__(self, tile_map: TileMap, grid: Grid) -> None:
        """Initialize the TileMapRenderer."""
        super().__init__()
        self.tile_map = tile_map
        self.grid = grid

    @override
    def render(self, position: Position, surface: pygame.Surface, *, rotation: Rotation | None = None) -> None:
        """Render the TileMap."""
        min_x, max_x, min_y, max_y = 0, self.tile_map.width, 0, self.tile_map.height

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                tile = self.tile_map.get_tile_at_coordinate(x, y)
                if tile:
                    # convert using grid
                    world_coords = self.grid.cell_to_world(Vector2(x, y))

                    # figure out the actual drawing
                    surface.blit(self.get_tile_surface(tile, self.grid.cell_size), world_coords.as_int_tuple())

    def get_tile_surface(self, tile: Tile, tile_size: int) -> pygame.Surface:
        """Get the surface of the Tile to draw."""
        surface = (
            tile.sprite.load()
            if tile.sprite is not None
            else SpriteImage.get_default_sprite_surface((tile_size, tile_size))
        )

        tile.material.apply(surface)
        return surface
