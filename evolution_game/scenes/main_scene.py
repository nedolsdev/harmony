"""The main scene for the evolution game."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.render_layer import RenderLayer
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.camera.camera_component import Camera, Viewport
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager


def create_main_scene(window_size: tuple[int, int], layers: SortingLayerManager) -> Scene:
    """Return the main scene for the evolution game."""
    scene = Scene()

    default_layer = layers.get_layer("Default")

    camera = (
        GameObjectBuilder(Empty)
        .add_component(Transform())
        .add_component(
            Camera(
                Viewport(
                    window_size[0],
                    window_size[1],
                ),
            ),
        )
        .add_component(RenderLayer(default_layer))
        .build()
    )

    scene.add_game_object(camera)

    return scene
