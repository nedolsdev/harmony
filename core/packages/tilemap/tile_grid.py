"""TileGrid encapsulates the tile map, grid, palette and renderer into a single class."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.tilemap.grid import Grid
    from core.packages.tilemap.tile_map import TileMap
    from core.packages.tilemap.tile_map_renderer import TileMapRenderer
    from core.packages.tilemap.tile_palette import TilePalette


class TileGrid:
    """TileGrid encapsulates the tile map, grid, palette and renderer into a single class."""

    def __init__(self, grid: Grid, tile_map: TileMap, tile_map_renderer: TileMapRenderer, palette: TilePalette) -> None:
        """Initialize the TileGrid."""
        self.grid = grid
        self.tile_map = tile_map
        self.tile_map_renderer = tile_map_renderer
        self.palette = palette
