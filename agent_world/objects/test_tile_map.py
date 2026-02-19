"""Test tile map."""

import random

from core.packages.tilemap.grid import Grid, HexGridSystem, SquareGridSystem
from core.packages.tilemap.tile import Tile
from core.packages.tilemap.tile_map import DictBasedTileMap
from core.packages.tilemap.tile_map_renderer import TileMapRenderer
from core.packages.tilemap.tile_palette import TilePalette
from game.material import ColorMaterial

grid = Grid(cell_size=16, system=HexGridSystem())

width = 16
height = 16

tile_map = DictBasedTileMap("Test TileMap", width, height)

white_tile = Tile(sprite=None, material=ColorMaterial(color=(255, 255, 255)))
black_tile = Tile(sprite=None, material=ColorMaterial(color=(0, 0, 0)))
red_tile = Tile(sprite=None, material=ColorMaterial(color=(255, 0, 0)))
green_tile = Tile(sprite=None, material=ColorMaterial(color=(0, 255, 0)))
blue_tile = Tile(sprite=None, material=ColorMaterial(color=(0, 0, 255)))

palette = TilePalette()
palette.add_tile(white_tile)
palette.add_tile(black_tile)
palette.add_tile(red_tile)
palette.add_tile(green_tile)
palette.add_tile(blue_tile)

for x in range(width):
    for y in range(height):
        random_tile = random.choice(palette.tiles)  # noqa: S311 (can be insecure)
        tile_map.set_tile(random_tile, x, y)


tile_map_renderer = TileMapRenderer(tile_map, grid)
