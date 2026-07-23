"""Create a test camera object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.camera.camera_component import Camera, Viewport
from harmony.core.packages.camera.camera_controller import CameraController
from harmony.core.packages.render.render_layer import RenderLayer
from harmony.game.material import GrayscaleMaterial
from harmony.game.object_builder import GameObjectBuilder

if TYPE_CHECKING:
    from harmony.game.object import GameObject
    from harmony.game.sorting_layer import SortingLayer
    from harmony.game.window import WindowSettings


def create_camera_game_object(window_settings: WindowSettings, layer: SortingLayer) -> GameObject:
    """Create a test camera object."""
    width, height = window_settings.world_resolution or window_settings.window_size
    return (
        GameObjectBuilder(Empty)
        .add_component(Transform())
        .add_component(
            Camera(
                Viewport(
                    width,
                    height,
                ),
                GrayscaleMaterial(),
            ),
        )
        .add_component(RenderLayer(layer))
        .add_component(CameraController(speed=50))
        .build()
    )
