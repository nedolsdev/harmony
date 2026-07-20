"""Timer example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from example_scenes.helpers.camera_util import create_camera_game_object
from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.timing.timer import ComponentUsingTimer
from harmony.game.object_builder import GameObjectBuilder
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_timer_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing timer behavior."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    # timer object
    timer_obj = GameObjectBuilder(Empty).add_component(Transform()).add_component(ComponentUsingTimer()).build()

    scene.add_game_object(timer_obj)

    scene.add_game_object(create_camera_game_object(window_settings, default_layer))

    return scene
