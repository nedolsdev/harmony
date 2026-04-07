"""A collection of Tiles that can be used to create a TileMap."""
from __future__ import annotations

from core.packages.tilemap.tile import Tile
from game.asset import Asset


class TilePalette(Asset):
    """A collection of Tiles that can be used to create a TileMap."""

    def __init__(self) -> None:
        """Initialize an empty TilePalette."""
        self.tiles: list[Tile] = []

    def add_tile(self, tile: Tile) -> None:
        """Add tile."""
        self.tiles.append(tile)

    def get_tile(self, index: int) -> Tile:
        """Get a tile at a given index."""
        if index < 0 or index > len(self.tiles):
            msg = "Out of range tile index for TilePalette."
            raise IndexError(msg)

        return self.tiles[index]
