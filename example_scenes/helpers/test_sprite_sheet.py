"""Test tile map."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from harmony.core.packages.tilemap.grid import Grid, SquareGridSystem
from harmony.core.packages.tilemap.tile_grid import TileGrid
from harmony.core.packages.tilemap.tile_map import DictBasedTileMap
from harmony.core.packages.tilemap.tile_map_renderer import TileMapRenderer
from harmony.core.packages.tilemap.tile_palette import TilePalette

if TYPE_CHECKING:
    from harmony.core.packages.spritesheet.sprite_sheet import SpriteSheet


def get_sprite_sheet_grid(
    sprite_sheet: SpriteSheet,
    cell_size: int = 64,
    gap: int = 0,
    width: int = 16,
    height: int = 16,
) -> TileGrid:
    """Get an example tile grid for testing the sprite sheet."""
    system = SquareGridSystem()

    grid = Grid(cell_size=cell_size, system=system, gap=gap)

    tile_map = DictBasedTileMap("Test TileMap", width, height)

    palette = TilePalette.from_sprite_sheet(sprite_sheet)

    for x in range(width):
        for y in range(height):
            random_tile = random.choice(palette.tiles)  # noqa: S311 (is not security sensitive)
            tile_map.set_tile(random_tile, x, y)

    tile_map_renderer = TileMapRenderer(tile_map, grid)

    return TileGrid(grid, tile_map, tile_map_renderer, palette)
