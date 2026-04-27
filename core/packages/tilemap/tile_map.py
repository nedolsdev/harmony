"""Defines an arrangement of Tiles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from game.component import GameComponent

if TYPE_CHECKING:
    from core.packages.tilemap.tile import Tile
    from game.event_handler import EventHandler


class TileMap(GameComponent, ABC):
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

    @abstractmethod
    def set_tile(self, tile: Tile, x: int, y: int) -> None:
        """Set a tile at a given coordinate."""

    @abstractmethod
    def remove_tile_at_coordinate(self, x: int, y: int) -> None:
        """Remove a tile at a given coordinate."""

    @abstractmethod
    def get_tile_at_coordinate(self, x: int, y: int) -> Tile | None:
        """Get a tile at a given coordinate."""

    def get_width(self) -> int:
        """Get an upper bound of the width (assumes the TileMap only grows)."""
        return self.width

    def get_height(self) -> int:
        """Get an upper bound of the width (assumes the TileMap only grows)."""
        return self.height

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

    def get_tile_at_coordinate(self, x: int, y: int) -> Tile | None:
        """Get a tile at a given coordinate."""
        if not self.in_bounds(x, y):
            return None
        return self.tiles.get((x, y), None)

    @override
    def copy(self) -> DictBasedTileMap:
        """Create a copy of the position component."""
        # TODO:  # noqa: TD003
        return self
