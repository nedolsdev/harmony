"""Collision example scene."""

from agent_world.components.rotate_around import RotateAround
from core.components.render_layer import RenderLayer
from core.components.sprite_2d import Sprite2D
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.collision.collider_rect import ColliderRect
from core.packages.collision.collision_grouper import CollisionGrouper
from core.packages.collision.collision_layer import CollisionLayer
from core.packages.collision.collision_rule import CollisionRule
from core.packages.collision.collision_test import CollisionTest
from core.packages.geometry.rectangle import Rectangle
from core.packages.geometry.vector2 import Vector2
from example_scenes.camera_util import create_camera_game_object
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.scene import Scene
from game.sorting_layer import SortingLayerManager


def create_collision_scene(window_size: int, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing collisions."""
    scene = Scene("Collision Scene")

    default_layer = layers.get_layer("Default")

    # collision layer and rule
    collision_layer = CollisionLayer("TestLayer")
    scene.collision_manager.add_collision_layer(collision_layer)
    scene.collision_manager.add_rule(
        CollisionRule(collision_layer, CollisionGrouper(), can_collide_with_self=True),
    )

    # rotating parent
    rotation_parent = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(300, 300)))
        .add_component(RenderLayer(default_layer))
        .add_component(RotateAround(2))
        .build()
    )

    # rotating square with collider
    collider1 = ColliderRect(Rectangle(25, 25, Vector2(0, 0)))
    collider1.add_layer(collision_layer)

    rotating_square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 0)))
        .add_component(Sprite2D(25, 25, ColorMaterial((255, 0, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(collider1)
        .build()
    )

    rotation_parent.add_child(rotating_square)
    scene.add_game_object(rotation_parent)

    # static square with collision test
    collider2 = ColliderRect(Rectangle(25, 25, Vector2(0, 0)))
    collider2.add_layer(collision_layer)

    static_square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(400, 300)))
        .add_component(Sprite2D(25, 25, ColorMaterial((0, 255, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(collider2)
        .add_component(CollisionTest())
        .build()
    )

    scene.add_game_object(static_square)

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
