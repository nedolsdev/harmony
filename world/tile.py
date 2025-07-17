"""Tile module for defining tile types and their properties in a grid."""

from enum import IntEnum


class TileType(IntEnum):
    """Defines constants for different tile types in the grid."""

    EMPTY = 0
    WALL = 1
    GOAL = 2
    HAZARD = 3
    AGENT = 4


TILE_COLORS: dict[TileType, tuple[int, int, int]] = {
    TileType.EMPTY: (255, 255, 255),
    TileType.WALL: (0, 0, 0),
    TileType.GOAL: (0, 200, 0),
    TileType.HAZARD: (200, 0, 0),
    TileType.AGENT: (0, 0, 255),
}


class Tile:
    """Represents a tile in the grid with a type and position."""

    def __init__(self, tile_type: TileType, x: int, y: int) -> None:
        """Initialize a tile with its type and position."""
        self.tile_type = tile_type
        self.x = x
        self.y = y
        color = TILE_COLORS.get(tile_type)

        if color is None:
            msg = f"Invalid tile type: {tile_type}"
            raise ValueError(msg)

        self.color = color
