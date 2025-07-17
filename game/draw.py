"""The draw module contains functions for rendering the game world visually."""

import pygame

from core.components.position import Position
from core.components.render import Render
from game.object import GameObject
from game.state import GameState


class Renderer:
    """Handles rendering of the game."""

    def __init__(self, title: str, window_width: int, window_height: int) -> None:
        """Initialize the renderer."""
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(title)

    def draw_objects(self, objects: list[GameObject]) -> None:
        """Draw game objects on the screen."""
        for obj in objects:
            if obj.has_component(Render) and obj.has_component(Position):
                render_component = obj.get_component(Render)
                position_component = obj.get_component(Position)
                render_component.render(position_component, self.screen)

    def draw_frame(self, state: GameState) -> None:
        """Draw a single frame of the game."""
        self.screen.fill((255, 255, 255))

        self.draw_objects(state.get_game_objects())

        pygame.display.flip()
