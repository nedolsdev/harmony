"""Timer example scene."""

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.timing.timer import ComponentUsingTimer
from example_scenes.camera_util import create_camera_game_object
from game.object_builder import GameObjectBuilder
from game.scene import Scene
from game.sorting_layer import SortingLayerManager


def create_timer_scene(window_size: int, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing timer behavior."""
    scene = Scene("Timer Scene")

    default_layer = layers.get_layer("Default")

    # timer object
    timer_obj = GameObjectBuilder(Empty).add_component(Transform()).add_component(ComponentUsingTimer()).build()

    scene.add_game_object(timer_obj)

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
