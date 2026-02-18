"""A collection of Tiles that can be used to create a TileMap."""

from core.packages.tilemap.tile import Tile


class TilePalette:
    """A collection of Tiles that can be used to create a TileMap."""

    def __init__(self) -> None:
        """Initialize an empty TilePalette."""
        self.tiles: list[Tile] = []

    def add_tile(self, tile: Tile) -> None:
        """Add tile."""
        self.tiles.append(tile)
