"""Custom render component for rendering grid tiles."""

from typing import override

import pygame

from core.components.position import Position
from core.components.render import Render
from core.components.rotation import Rotation
from core.objects.grid import Grid


class GridRender(Render):
    """Render component for grid tiles."""

    def __init__(self, grid: Grid) -> None:
        """Initialize the grid render component."""
        super().__init__()
        self.grid = grid

    @override
    def render(self, position: Position, surface: pygame.Surface, *, rotation: Rotation | None = None) -> None:
        """Render the tile at the specified position."""
        for y in range(self.grid.grid_size):
            for x in range(self.grid.grid_size):
                tile = self.grid.tiles[y][x]
                color = tile.color
                rect = pygame.Rect(
                    x * self.grid.tile_size,
                    y * self.grid.tile_size,
                    self.grid.tile_size,
                    self.grid.tile_size,
                )
                pygame.draw.rect(surface, color, rect)

                # draw grid lines
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Start the render component."""

    @override
    def update(self) -> None:
        """Update the render component."""
