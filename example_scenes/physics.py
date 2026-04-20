"""Physics example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.render_layer import RenderLayer
from core.components.sprite_2d import Sprite2D
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from core.packages.physics.rigidbody_2d import RigidBody2D
from example_scenes.camera_util import create_camera_game_object
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager


def create_physics_scene(window_size: int, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing physics."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(Vector2(100, 100)))
        .add_component(Sprite2D(25, 25, ColorMaterial((0, 255, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(RigidBody2D(velocity=Vector2(10, 0)))
        .build()
    )

    scene.add_game_object(square)

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
