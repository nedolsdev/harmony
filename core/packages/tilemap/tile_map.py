"""Defines an arrangement of Tiles."""

from core.packages.tilemap.tile import Tile
from game.component import GameComponent


class TileMap(GameComponent):
    """Defines an arrangement of Tiles."""

    def __init__(self, name: str) -> None:
        """Initialize the TileMap component."""
        super().__init__()
        self.name = name

    def set_tile(self, tile: Tile, x: int, y: int) -> None:
        """Set a tile at a given coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    def remove_tile_at_coordinate(self, x: int, y: int) -> None:
        """Remove a tile at a given coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    def get_tile_at_coordinate(self, x: int, y: int) -> Tile:
        """Get a tile at a given coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)


class DictBasedTileMap(TileMap):
    """Defines an arrangement of Tiles stored as dict with coordinate keys."""

    # TODO: Add chunking  # noqa: TD003

    def __init__(self, name: str) -> None:
        """Initialize the DictBasedTileMap."""
        super().__init__(name)
        self.tiles: dict[tuple[int, int], Tile] = {}

    def set_tile(self, tile: Tile, x: int, y: int) -> None:
        """Set a tile at a given coordinate."""
        self.tiles[(x, y)] = tile

    def remove_tile_at_coordinate(self, x: int, y: int) -> None:
        """Remove a tile at a given coordinate."""
        del self.tiles[(x, y)]

    def get_tile_at_coordinate(self, x: int, y: int) -> Tile:
        """Get a tile at a given coordinate."""
        return self.tiles[(x, y)]
