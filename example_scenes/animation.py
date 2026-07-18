"""Animation example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from core.packages.render.render_layer import RenderLayer
from core.packages.render.sprite_2d import Sprite2D
from core.packages.timing.delta_time import DeltaTime
from example_scenes.helpers.camera_util import create_camera_game_object
from example_scenes.helpers.test_animation import create_test_animator
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager
    from game.window import WindowSettings


def create_animation_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing animations."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    DeltaTime().set_time_scale(scale=4)

    static_square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(400, 300)))
        .add_component(Sprite2D(25, 25, ColorMaterial((0, 255, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(create_test_animator())
        .build()
    )

    scene.add_game_object(static_square)

    scene.add_game_object(create_camera_game_object(window_settings, default_layer))

    return scene
