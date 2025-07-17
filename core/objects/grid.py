"""The world grid module defines the grid size and tiles used in the game world."""

import random

from core.objects.tile import Tile, TileType
from game.event_handler import EventHandler
from game.object import GameObject


class Grid(GameObject):
    """Represents a grid of tiles in the game world."""

    def __init__(self, grid_size: int) -> None:
        """Initialize the grid with empty tiles."""
        super().__init__()
        self.grid_size = grid_size

        self.tiles = [[Tile(TileType.EMPTY, x, y) for x in range(self.grid_size)] for y in range(self.grid_size)]
        self.tags.add("grid")

    def set_tile(self, x: int, y: int, tile_type: TileType) -> None:
        """Set the tile at the specified position to the given tile type."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.tiles[y][x] = Tile(tile_type, x, y)
        else:
            msg = f"Coordinates ({x}, {y}) out of bounds for grid size {self.grid_size}."
            raise IndexError(msg)

    def add_events(self, event_handler: EventHandler) -> None:
        """Register event listeners for the grid."""


class GridGenerator:
    """Generates a grid with random tiles."""

    @staticmethod
    def generate(grid_size: int) -> Grid:
        """Generate a grid with random tiles."""
        grid = Grid(grid_size)

        chance_wall = 0.1
        chance_hazard = 0.1

        for y in range(grid.grid_size):
            for x in range(grid.grid_size):
                if (x, y) == (grid.grid_size - 1, grid.grid_size - 1):
                    grid.set_tile(x, y, TileType.GOAL)
                else:
                    rnd = random.random()  # noqa: S311 (not security-sensitive)
                    if rnd < chance_wall:
                        grid.set_tile(x, y, TileType.WALL)
                    elif rnd < chance_wall + chance_hazard:
                        grid.set_tile(x, y, TileType.HAZARD)
                    else:
                        grid.set_tile(x, y, TileType.EMPTY)
        return grid
