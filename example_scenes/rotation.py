"""Rotation example scene."""
from __future__ import annotations

from typing import TYPE_CHECKING

from agent_world.components.rotate_around import RotateAround
from core.components.render_layer import RenderLayer
from core.components.sprite_2d import Sprite2D
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from example_scenes.camera_util import create_camera_game_object
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager


def create_rotation_scene(window_size: int, layers: SortingLayerManager) -> Scene:
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
        .add_component(Sprite2D(25, 25, ColorMaterial((255, 0, 0))))
        .add_component(RenderLayer(default_layer))
        .build()
    )

    rotation_parent.add_child(square)

    scene.add_game_object(rotation_parent)

    scene.add_game_object(create_camera_game_object(window_size, layers.get_layer("Default")))

    return scene
