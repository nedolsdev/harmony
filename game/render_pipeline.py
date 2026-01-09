"""The draw module contains functions for rendering the game world visually."""

import pygame

from core.components.position import Position
from core.components.render import Render
from core.components.render_layer import RenderLayer
from game.object import GameObject
from game.scene import Scene
from game.sorting_layer import SortingLayerManager


class RenderPipeline:
    """Handles rendering of the game."""

    def __init__(self, title: str, window_width: int, window_height: int) -> None:
        """Initialize the renderer."""
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.sorting_layers = SortingLayerManager()
        pygame.display.set_caption(title)

    def draw_objects(self, objects: list[GameObject]) -> None:
        """Draw game objects on the screen."""
        # NOTE: This will be called only on objects with Render components
        # and it will be pre-sorted by the scene's render queue.

        for obj in objects:
            render_component = obj.get_component(Render)
            position_component = obj.get_component(Position)
            render_component.render(position_component, self.screen)

    def draw_frame(self, scene: Scene) -> None:
        """Draw a single frame of the game."""
        self.screen.fill((255, 255, 255))

        self.draw_objects(self.get_render_queue(scene))

        pygame.display.flip()

    def get_render_queue(self, scene: Scene) -> list[GameObject]:
        """Get a list of game objects sorted by their sorting layer and order in layer for rendering."""
        game_objects = scene.get_flattened_game_objects()

        # can render and is active
        to_render: list[GameObject] = []

        for i, obj in enumerate(game_objects):
            if (
                obj.active
                and obj.has_component(Render)
                and obj.get_component(Render).active
                and obj.has_component(RenderLayer)
                and obj.has_component(Position)
            ):
                to_render.append(obj)
                render_layer = obj.get_component(RenderLayer)
                render_layer.set_order_in_layer(i)

        # sort by sorting layer value and order in layer
        def sort_key(game_object: GameObject) -> tuple[int, int]:
            render_layer = game_object.get_component(RenderLayer)
            sorting_layer = render_layer.sorting_layer
            return (sorting_layer.value, render_layer.order_in_layer or 0)

        to_render.sort(key=sort_key)
        return to_render
