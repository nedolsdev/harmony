"""The draw module contains functions for rendering the game world visually."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from harmony.core.components.transform import Transform
from harmony.core.packages.camera.camera_component import Camera
from harmony.core.packages.render.primitive_renderer import PygamePrimitiveRenderer
from harmony.core.packages.render.render import Render
from harmony.core.packages.render.render_layer import RenderLayer
from harmony.game.sorting_layer import SortingLayerManager
from harmony.game.window import GameWindow, WindowSettings

if TYPE_CHECKING:
    from harmony.core.packages.render.primitive import RenderPrimitive
    from harmony.core.packages.render.resolution import ResolutionManager
    from harmony.game.object import GameObject
    from harmony.game.scene import Scene


class NoCameraError(RuntimeError):
    """Exception raised when no camera exists in the scene."""


class RenderPipeline:
    """Handles rendering of the game."""

    def __init__(
        self,
        resolution: ResolutionManager,
        window_settings: WindowSettings | None = None,
        default_fill_color: tuple[int, int, int] | tuple[int, int, int, int] = (0, 0, 0),
    ) -> None:
        """Initialize the renderer."""
        self.window = GameWindow(resolution, window_settings)
        self.sorting_layers = SortingLayerManager()
        self._default_fill_color = default_fill_color

    def draw_objects(self, objects: list[GameObject], cameras: list[Camera]) -> pygame.Surface:
        """Draw game objects on the screen."""
        # NOTE: This will be called only on objects with Render components
        # and it will be pre-sorted by the scene's render queue.

        # if there are no cameras then there is no point drawing anything
        if len(cameras) == 0:
            msg = "There are no active cameras in the scene."
            raise NoCameraError(msg)

        # TODO: Fix performance here, matrixes / other point mapping to avoid looping for each camera  # noqa: TD003

        logical_surface = self.window.get_logical_surface()

        world_space: list[RenderPrimitive] = []

        for obj in objects:
            transform = obj.get_component(Transform)
            for render_component in obj.get_components_of_type(Render):
                world_space.extend(render_component.render(transform))

        camera_space: list[RenderPrimitive] = []
        for camera in cameras:
            for primitive in world_space:
                camera_space.append(primitive.transform(camera.transform))  # noqa: PERF401

        PygamePrimitiveRenderer(logical_surface).render_primitives(camera_space)

        return logical_surface

    def draw_frame(self, scene: Scene) -> None:
        """Draw a single frame of the game."""
        screen = self.window.get_screen_surface()

        screen.fill(self._default_fill_color)

        objects, cameras = self.get_render_queue(scene)

        surface = self.draw_objects(objects, cameras)

        self.window.apply_to_screen(surface)

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
