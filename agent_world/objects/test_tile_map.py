"""Test tile map."""

import random

from core.assets.polygon_asset import PolygonAsset
from core.packages.geometry.polygon import Polygon
from core.packages.geometry.rectangle import Rectangle
from core.packages.tilemap.grid import Grid, HexGridSystem, SquareGridSystem
from core.packages.tilemap.tile import Tile
from core.packages.tilemap.tile_map import DictBasedTileMap
from core.packages.tilemap.tile_map_renderer import TileMapRenderer
from core.packages.tilemap.tile_palette import TilePalette
from game.material import ColorMaterial
from game.vector2 import Vector2

cell_size = 64

grid = Grid(cell_size=cell_size, system=HexGridSystem(), gap=0)

width = 16
height = 16

tile_map = DictBasedTileMap("Test TileMap", width, height)

square_polygon = Rectangle(cell_size, cell_size, Vector2.zero())

hex_polygon = Polygon.regular(6, cell_size // 2, rotation_degrees=30)

surface = PolygonAsset(
    polygon=hex_polygon,
    fill_color=(255, 255, 255),
    outline_width=2,
    outline_color=(144, 144, 144),
)


white_tile = Tile(tile_surface=surface.copy(), material=ColorMaterial(color=(255, 255, 255)))
black_tile = Tile(tile_surface=surface.copy(), material=ColorMaterial(color=(0, 0, 0)))
red_tile = Tile(tile_surface=surface.copy(), material=ColorMaterial(color=(255, 0, 0)))
green_tile = Tile(tile_surface=surface.copy(), material=ColorMaterial(color=(0, 255, 0)))
blue_tile = Tile(tile_surface=surface.copy(), material=ColorMaterial(color=(0, 0, 255)))

palette = TilePalette()
palette.add_tile(black_tile)
palette.add_tile(red_tile)
palette.add_tile(green_tile)
palette.add_tile(blue_tile)


for x in range(width):
    for y in range(height):
        random_tile = random.choice(palette.tiles)  # noqa: S311 (is not security sensitive)
        tile_map.set_tile(random_tile, x, y)

tile_map_renderer = TileMapRenderer(tile_map, grid)
