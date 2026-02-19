"""The Grid component defines a local coordinate system for positioning cells."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

from game.component import GameComponent
from game.sorting_layer import SortingLayerManager
from game.vector2 import Vector2

if TYPE_CHECKING:
    from core.packages.tilemap.tile_map import TileMap
    from game.event_handler import EventHandler


class GridSystem:
    """Defines the coordinate system of a Grid."""

    def world_to_cell(self, world_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    def cell_to_world(self, cell_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)

    def get_neighbors(self, cell_coord: Vector2) -> list[Vector2]:
        """Get the neighbors of a given cell coordinate."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)


class SquareGridSystem(GridSystem):
    """A square coordinate system for a Grid."""

    def world_to_cell(self, world_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        return world_coord // cell_size

    def cell_to_world(self, cell_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        return cell_coord * cell_size

    def get_neighbors(self, cell_coord: Vector2) -> list[Vector2]:
        """Get the neighbors of a given cell coordinate."""
        x, y = cell_coord.x, cell_coord.y
        return [
            Vector2(x + 1, y),
            Vector2(x - 1, y),
            Vector2(x, y + 1),
            Vector2(x, y - 1),
        ]


class HexGridSystem(GridSystem):
    """A hexagonal coordinate system for a Grid. (Axial coordinates with Pointy Hexes)."""

    def world_to_cell(self, world_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        size = cell_size

        q = (math.sqrt(3) / 3 * world_coord.x - 1 / 3 * world_coord.y) / size
        r = (2 / 3 * world_coord.y) / size

        return self._hex_round(q, r)

    def cell_to_world(self, cell_coord: Vector2, cell_size: int) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        size = cell_size
        q, r = cell_coord.x, cell_coord.y

        x = size * (math.sqrt(3) * q + math.sqrt(3) / 2 * r)
        y = size * (3 / 2 * r)

        return Vector2(x, y)

    def get_neighbors(self, cell_coord: Vector2) -> list[Vector2]:
        """Get the neighbors of a given cell coordinate."""
        q, r = cell_coord.x, cell_coord.y
        return [
            Vector2(q + 1, r),
            Vector2(q + 1, r - 1),
            Vector2(q, r - 1),
            Vector2(q - 1, r),
            Vector2(q - 1, r + 1),
            Vector2(q, r + 1),
        ]

    def _hex_round(self, q: float, r: float) -> Vector2:
        # convert axial coord to cube coord
        x = q
        z = r
        y = -x - z

        rx = round(x)
        ry = round(y)
        rz = round(z)

        x_diff = abs(rx - x)
        y_diff = abs(ry - y)
        z_diff = abs(rz - z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        # convert back
        return Vector2(int(rx), int(rz))


class Grid(GameComponent):
    """The Grid component defines a local coordinate system for positioning cells."""

    # TODO: Add grid gap  # noqa: TD003

    def __init__(self, cell_size: int, system: GridSystem) -> None:
        """Initialize the Grid component."""
        super().__init__()
        self.cell_size = cell_size
        self.system = system
        self.layers = SortingLayerManager()

        # tile maps keyed by their name
        self.tile_maps: dict[str, TileMap] = {}

    def add_tile_map(self, tile_map: TileMap, layer: int) -> None:
        """Create a TileMap at a given Z-layer on the Grid."""
        self.layers.create_layer(tile_map.name, layer)

    def world_to_cell(self, world_coord: Vector2) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        return self.system.world_to_cell(world_coord, self.cell_size)

    def cell_to_world(self, cell_coord: Vector2) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        return self.system.cell_to_world(cell_coord, self.cell_size)

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def copy(self) -> Grid:
        """Create a copy of the position component."""
        # TODO:  # noqa: TD003
        return self
