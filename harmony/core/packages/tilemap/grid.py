"""The Grid component defines a local coordinate system for positioning cells."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.vector2 import Vector2
from harmony.game.component import GameComponent
from harmony.game.sorting_layer import SortingLayerManager

if TYPE_CHECKING:
    from harmony.core.packages.tilemap.tile_map import TileMap
    from harmony.game.event_handler import EventHandler


class GridSystem(ABC):
    """Defines the coordinate system of a Grid."""

    @abstractmethod
    def world_to_cell(self, world_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the world coordinate to cell coordinate."""

    @abstractmethod
    def cell_to_local(self, cell_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the cell coordinate to local coordinate."""

    @abstractmethod
    def get_neighbors(self, cell_coord: Vector2) -> list[Vector2]:
        """Get the neighbors of a given cell coordinate."""


class SquareGridSystem(GridSystem):
    """A square coordinate system for a Grid."""

    def world_to_cell(self, world_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        return world_coord // (cell_size + gap)

    def cell_to_local(self, cell_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        return cell_coord * (cell_size + gap)

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

    def world_to_cell(self, world_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        size = (cell_size / 2) + gap

        q = (math.sqrt(3) / 3 * world_coord.x - 1 / 3 * world_coord.y) / size
        r = (2 / 3 * world_coord.y) / size

        return self._hex_round(q, r)

    def cell_to_local(self, cell_coord: Vector2, cell_size: float, gap: float) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        size = (cell_size / 2) + gap
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

    def __init__(self, cell_size: float, system: GridSystem, gap: float = 0) -> None:
        """Initialize the Grid component."""
        super().__init__()
        self.cell_size = cell_size
        self.gap = gap
        self.system = system
        self.layers = SortingLayerManager()

        # tile maps keyed by their name
        self.tile_maps: dict[str, TileMap] = {}

    def add_tile_map(self, tile_map: TileMap, layer: int) -> None:
        """Create a TileMap at a given Z-layer on the Grid."""
        self.layers.create_layer(tile_map.name, layer)

    def world_to_cell(self, world_coord: Vector2) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        return self.system.world_to_cell(world_coord, self.cell_size, self.gap)

    def cell_to_local(self, cell_coord: Vector2) -> Vector2:
        """Convert the cell coordinate to local coordinate."""
        return self.system.cell_to_local(cell_coord, self.cell_size, self.gap)

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
    def fixed_update(self) -> None:
        """Update the sprite component on fixed physics step."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def copy(self) -> Grid:
        """Create a copy of the position component."""
        # TODO:  # noqa: TD003
        return self
