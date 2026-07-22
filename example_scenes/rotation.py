"""Rotation example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from example_scenes.helpers.camera_util import create_camera_game_object
from example_scenes.helpers.rotate_around import RotateAround
from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.geometry.rectangle import Rectangle
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.rect_render_2d import RectRender2D
from harmony.core.packages.render.render_layer import RenderLayer
from harmony.game.object_builder import GameObjectBuilder
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_rotation_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing rotation behavior."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    # rotating parent object
    rotation_parent = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(400, 400), local_scale=Vector2(2, 2)))
        .add_component(RenderLayer(default_layer))
        .add_component(RotateAround(2))
        .build()
    )

    # child square that rotates
    square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 0), local_scale=Vector2(2, 2)))
        .add_component(RectRender2D(Rectangle(25, 25, Vector2(0, 0)), (255, 0, 0)))
        .add_component(RenderLayer(default_layer))
        .build()
    )

    rotation_parent.add_child(square)

    scene.add_game_object(rotation_parent)

    scene.add_game_object(create_camera_game_object(window_settings, layers.get_layer("Default")))

    return scene
