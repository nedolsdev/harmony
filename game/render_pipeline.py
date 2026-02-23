"""The draw module contains functions for rendering the game world visually."""

import pygame

from core.components.render import Render
from core.components.render_layer import RenderLayer
from core.components.transform import Transform
from core.packages.camera.camera_component import Camera
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

    def draw_objects(self, objects: list[GameObject], cameras: list[Camera]) -> None:
        """Draw game objects on the screen."""
        # NOTE: This will be called only on objects with Render components
        # and it will be pre-sorted by the scene's render queue.

        # if there are no cameras then there is no point drawing anything
        if len(cameras) == 0:
            msg = "There are no active cameras in the scene."
            raise ValueError(msg)

        # TODO: Fix performance here, matrixes / other point mapping to avoid looping for each camera  # noqa: TD003

        for camera in cameras:
            camera_surface = self.screen.subsurface(camera.viewport.as_tuple())
            for obj in objects:
                transform = obj.get_component(Transform)
                for render_component in obj.get_components_of_type(Render):
                    render_component.render(transform, camera_surface, camera)

    def draw_frame(self, scene: Scene) -> None:
        """Draw a single frame of the game."""
        self.screen.fill((255, 255, 255))

        objects, cameras = self.get_render_queue(scene)

        self.draw_objects(objects, cameras)

        pygame.display.flip()

    def get_render_queue(self, scene: Scene) -> tuple[list[GameObject], list[Camera]]:
        """Get a list of game objects sorted by their sorting layer and order in layer for rendering."""
        game_objects = scene.get_flattened_game_objects()

        # can render and is active
        to_render: list[GameObject] = []

        # cameras
        cameras: list[Camera] = []

        for i, obj in enumerate(game_objects):
            # add camera
            if obj.active and obj.has_component(Camera):
                cameras.append(obj.get_component(Camera))

            # add object that could be rendered
            if (
                obj.active
                and obj.has_component(Render)
                and obj.get_component(Render).active
                and obj.has_component(RenderLayer)
                and obj.has_component(Transform)
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
        return to_render, cameras
