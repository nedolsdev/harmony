"""The Grid component defines a local coordinate system for positioning cells."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from game.component import GameComponent
from game.sorting_layer import SortingLayerManager

if TYPE_CHECKING:
    from core.packages.tilemap.tile_map import TileMap
    from game.event_handler import EventHandler
    from game.vector2 import Vector2


class Grid(GameComponent):
    """The Grid component defines a local coordinate system for positioning cells."""

    def __init__(self, cell_size: int) -> None:
        """Initialize the Grid component."""
        super().__init__()
        self.cell_size = cell_size
        self.layers = SortingLayerManager()

        # tile maps keyed by their name
        self.tile_maps: dict[str, TileMap] = {}

    def add_tile_map(self, tile_map: TileMap, layer: int) -> None:
        """Create a TileMap at a given Z-layer on the Grid."""
        self.layers.create_layer(tile_map.name, layer)

    def world_to_cell(self, world_coord: Vector2) -> Vector2:
        """Convert the world coordinate to cell coordinate."""
        return world_coord // self.cell_size

    def cell_to_world(self, cell_coord: Vector2) -> Vector2:
        """Convert the cell coordinate to world coordinate."""
        return cell_coord * self.cell_size

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
