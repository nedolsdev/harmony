"""The draw module contains functions for rendering the game world visually."""

import pygame

from core.components.mesh_2d import Mesh2D
from core.components.position import Position
from core.objects.grid import Grid
from game.object import GameObject
from game.state import GameState


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
        for y in range(grid.grid_size):
            for x in range(grid.grid_size):
                tile = grid.tiles[y][x]
                color = tile.color
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                # draw grid lines
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_objects(self, objects: list[GameObject]) -> None:
        """Draw game objects on the screen."""
        for obj in objects:
            if obj.has_component(Mesh2D) and obj.has_component(Position):
                mesh = obj.get_component(Mesh2D)
                pos = obj.get_component(Position).get_coordinates()
                rect = pygame.Rect(pos[0] * self.TILE_SIZE, pos[1] * self.TILE_SIZE, mesh.width, mesh.height)
                pygame.draw.rect(self.screen, mesh.material.color, rect)

    def draw_frame(self, state: GameState) -> None:
        """Draw a single frame of the game."""
        self.screen.fill((255, 255, 255))

        grid = state.find_with_tag("grid")[0]

        if not isinstance(grid, Grid):
            msg = "Expected a Grid object with tag 'grid'."
            raise TypeError(msg)

        self.draw_grid(grid)
        self.draw_objects(state.get_game_objects())

        pygame.display.flip()
