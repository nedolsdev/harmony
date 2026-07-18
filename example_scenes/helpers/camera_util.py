"""Create a test camera object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.camera.camera_component import Camera, Viewport
from core.packages.camera.camera_controller import CameraController
from core.packages.render.render_layer import RenderLayer
from game.object_builder import GameObjectBuilder

if TYPE_CHECKING:
    from game.object import GameObject
    from game.sorting_layer import SortingLayer
    from game.window import WindowSettings


def create_camera_game_object(window_settings: WindowSettings, layer: SortingLayer) -> GameObject:
    """Create a test camera object."""
    width, height = window_settings.resolution
    return (
        GameObjectBuilder(Empty)
        .add_component(Transform())
        .add_component(
            Camera(
                Viewport(
                    width,
                    height,
                ),
            ),
        )
        .add_component(RenderLayer(layer))
        .add_component(CameraController(speed=50))
        .build()
    )
