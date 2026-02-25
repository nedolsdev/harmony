"""The TileMapRenderer defines how the TileMap is drawn to the screen."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.components.render import Render
from game.vector2 import Vector2

if TYPE_CHECKING:
    from core.components.transform import Transform
    from core.packages.camera.camera_component import Camera
    from core.packages.tilemap.grid import Grid
    from core.packages.tilemap.tile import Tile
    from core.packages.tilemap.tile_map import TileMap
    from game.event_handler import EventHandler


class TileMapRenderer(Render):
    """The TileMapRenderer defines how the TileMap is drawn to the screen."""

    def __init__(self, tile_map: TileMap, grid: Grid) -> None:
        """Initialize the TileMapRenderer."""
        super().__init__()
        self.tile_map = tile_map
        self.grid = grid

    @override
    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the TileMap."""
        min_x, max_x, min_y, max_y = 0, self.tile_map.width, 0, self.tile_map.height

        local_size = Vector2(self.grid.cell_size, self.grid.cell_size)

        world_size = transform.transform_scale(local_size)

        screen_size = camera.transform.inverse_transform_scale(world_size)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                tile = self.tile_map.get_tile_at_coordinate(x, y)
                if tile:
                    # convert using grid
                    local_coords = self.grid.cell_to_local(Vector2(x, y))

                    world_coords = transform.transform_point(local_coords)

                    screen_coords = camera.world_to_screen(world_coords)

                    tile_surface = self.get_tile_surface(tile, screen_size)

                    # figure out the actual drawing
                    surface.blit(tile_surface, screen_coords.as_tuple())

    def get_tile_surface(self, tile: Tile, screen_size: Vector2) -> pygame.Surface:
        """Get the surface of the Tile to draw."""
        return pygame.transform.scale(tile.get_surface(), screen_size.as_tuple())

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
    def copy(self) -> TileMapRenderer:
        """Create a copy of the sprite component."""
        return TileMapRenderer(self.tile_map.copy(), self.grid.copy())
