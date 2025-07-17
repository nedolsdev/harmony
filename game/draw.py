"""The draw module contains functions for rendering the game world visually."""

import pygame

from world.grid import Grid
from world.state import GameState


class Renderer:
    """Handles rendering of the game world."""

    TILE_SIZE = 60

    def __init__(self, grid_size: int) -> None:
        """Initialize the renderer with a grid."""
        self.window_size = grid_size * self.TILE_SIZE

        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("2D Gridworld")

    def draw_grid(self, grid: Grid) -> None:
        """Draw the grid on the screen."""
        for y in range(grid.GRID_SIZE):
            for x in range(grid.GRID_SIZE):
                tile = grid.tiles[y][x]
                color = tile.color
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                # draw grid lines
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_frame(self, state: GameState) -> None:
        """Draw a single frame of the game."""
        self.screen.fill((255, 255, 255))
        self.draw_grid(state.grid)

        pygame.display.flip()
