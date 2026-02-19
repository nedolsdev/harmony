"""Defines an arrangement of Tiles."""

from core.packages.tilemap.tile import Tile
from game.component import GameComponent


class TileMap(GameComponent):
    """Defines an arrangement of Tiles."""

    def __init__(self, name: str, width: int, height: int) -> None:
        """Initialize the TileMap component."""
        super().__init__()
        self.name = name
        self.width = width
        self.height = height

    def in_bounds(self, x: int, y: int) -> bool:
        """Check whether the coordinate is in the bounds of the TileMap."""
        return self.width > x >= 0 and self.height > y >= 0

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

    def get_width(self) -> int:
        """Get an upper bound of the width (assumes the TileMap only grows)."""
        return self.width

    def get_height(self) -> int:
        """Get an upper bound of the width (assumes the TileMap only grows)."""
        return self.height


class DictBasedTileMap(TileMap):
    """Defines an arrangement of Tiles stored as dict with coordinate keys."""

    # TODO: Add chunking  # noqa: TD003

    def __init__(self, name: str, width: int, height: int) -> None:
        """Initialize the DictBasedTileMap."""
        super().__init__(name, width, height)
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
