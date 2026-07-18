"""Create a test camera object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.render_layer import RenderLayer
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.camera.camera_component import Camera, Viewport
from core.packages.camera.camera_controller import CameraController
from core.packages.geometry.vector2 import Vector2
from game.object_builder import GameObjectBuilder

if TYPE_CHECKING:
    from game.object import GameObject
    from game.sorting_layer import SortingLayer


def create_camera_game_object(window_size: int, layer: SortingLayer) -> GameObject:
    """Create a test camera object."""
    return (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_scale=Vector2(0.25, 0.25)))
        .add_component(
            Camera(
                Viewport(
                    window_size,
                    window_size,
                ),
            ),
        )
        .add_component(RenderLayer(layer))
        .add_component(CameraController(speed=50))
        .build()
    )
