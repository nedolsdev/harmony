"""UI example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Font

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from core.packages.render.render_layer import RenderLayer
from core.packages.ui.components.base.visual.text import Text
from example_scenes.helpers.camera_util import create_camera_game_object
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager


def create_ui_scene(window_size: int, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing the UI system."""
    scene = Scene()

    default_layer = layers.get_layer("UI")

    ui_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 100)))
        .add_component(Text(content="Hello World", font=Font(size=100), color=(0, 0, 0)))
        .add_component(RenderLayer(default_layer))
        .build()
    )

    scene.add_game_object(ui_obj)

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
