"""Physics collision combined scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from example_scenes.helpers.camera_util import create_camera_game_object
from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.collision.collider_rect import ColliderRect
from harmony.core.packages.collision.collision_grouper import CollisionGrouper
from harmony.core.packages.collision.collision_layer import CollisionLayer
from harmony.core.packages.collision.collision_rule import CollisionRule
from harmony.core.packages.geometry.rectangle import Rectangle
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.physics.rigidbody_2d import RigidBody2D
from harmony.core.packages.render.rect_render_2d import RectRender2D
from harmony.core.packages.render.render_layer import RenderLayer
from harmony.game.object_builder import GameObjectBuilder
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.core.packages.collision.collision_manager import CollisionManager
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_physics_collision_scene(
    window_settings: WindowSettings,
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
        .add_component(RectRender2D(Rectangle(25, 25, Vector2(0, 0)), (0, 255, 0)))
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
        .add_component(RectRender2D(Rectangle(25, 25, Vector2(0, 0)), (255, 0, 0)))
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

    scene.add_game_object(create_camera_game_object(window_settings, default_layer))

    return scene
