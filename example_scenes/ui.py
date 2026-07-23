"""UI example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Font

from example_scenes.helpers.camera_util import create_camera_game_object
from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.render_layer import RenderLayer
from harmony.core.packages.ui.components.base.visual.text import Text
from harmony.game.object_builder import GameObjectBuilder
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_ui_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing the UI system."""
    scene = Scene()

    default_layer = layers.get_layer("UI")

    ui_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 100)))
        .add_component(Text(content="Hello World", font=Font(size=100), color=(255, 255, 255), antialiased=True))
        .add_component(RenderLayer(default_layer))
        .build()
    )

    scene.add_game_object(ui_obj)

    scene.add_game_object(create_camera_game_object(window_settings, default_layer))

    return scene
