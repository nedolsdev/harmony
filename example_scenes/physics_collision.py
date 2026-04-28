"""Physics collision combined scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.collision.collider_rect import ColliderRect
from core.packages.collision.collision_grouper import CollisionGrouper
from core.packages.collision.collision_layer import CollisionLayer
from core.packages.collision.collision_rule import CollisionRule
from core.packages.geometry.rectangle import Rectangle
from core.packages.geometry.vector2 import Vector2
from core.packages.physics.rigidbody_2d import RigidBody2D
from core.packages.render.render_layer import RenderLayer
from core.packages.render.sprite_2d import Sprite2D
from example_scenes.helpers.camera_util import create_camera_game_object
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from core.packages.collision.collision_manager import CollisionManager
    from game.sorting_layer import SortingLayerManager


def create_physics_collision_scene(
    window_size: int,
    layers: SortingLayerManager,
    collision_manager: CollisionManager,
) -> Scene:
    """Physics collision combined scene."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    collision_layer = CollisionLayer("TestLayer")
    collision_manager.add_collision_layer(collision_layer)
    collision_manager.add_rule(
        CollisionRule(collision_layer, CollisionGrouper(), can_collide_with_self=True),
    )

    static_collider = ColliderRect(Rectangle(25, 25, Vector2(0, 0)))
    static_collider.add_layer(collision_layer)

    static_square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(400, 300), local_rotation=1.1))
        .add_component(Sprite2D(25, 25, ColorMaterial((0, 255, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(static_collider)
        .add_component(
            RigidBody2D(moment_of_inertia=0.9),
        )
        .build()
    )

    moving_collider = ColliderRect(Rectangle(25, 25, Vector2(0, 0)))
    moving_collider.add_layer(collision_layer)

    moving_square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 300)))
        .add_component(Sprite2D(25, 25, ColorMaterial((255, 0, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(moving_collider)
        .add_component(
            RigidBody2D(
                velocity=Vector2(200, 0),
                angular_velocity=10,
                angular_damping=0.1,
            ),
        )
        .build()
    )

    scene.add_game_object(static_square)
    scene.add_game_object(moving_square)

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
