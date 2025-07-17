"""The world grid module defines the grid size and tiles used in the game world."""

import random

from world.tile import Tile, TileType


class Grid:
    """Represents a grid of tiles in the game world."""

    GRID_SIZE = 10

    def __init__(self) -> None:
        """Initialize the grid with empty tiles."""
        self.tiles = [[Tile(TileType.EMPTY, x, y) for x in range(self.GRID_SIZE)] for y in range(self.GRID_SIZE)]

    def set_tile(self, x: int, y: int, tile_type: TileType) -> None:
        """Set the tile at the specified position to the given tile type."""
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
            self.tiles[y][x] = Tile(tile_type, x, y)
        else:
            msg = f"Coordinates ({x}, {y}) out of bounds for grid size {self.GRID_SIZE}."
            raise IndexError(msg)


class GridGenerator:
    """Generates a grid with random tiles."""

    @staticmethod
    def generate() -> Grid:
        """Generate a grid with random tiles."""
        grid = Grid()

        chance_wall = 0.1
        chance_hazard = 0.1

        for y in range(grid.GRID_SIZE):
            for x in range(grid.GRID_SIZE):
                if (x, y) == (grid.GRID_SIZE - 1, grid.GRID_SIZE - 1):
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
