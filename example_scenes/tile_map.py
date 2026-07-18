"""Tile map example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from core.packages.render.render_layer import RenderLayer
from example_scenes.helpers.camera_util import create_camera_game_object
from example_scenes.helpers.test_tile_map import get_example_tile_grid
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager
    from game.window import WindowSettings


def create_tile_map_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing the tile map."""
    scene = Scene()

    tile_grid = get_example_tile_grid()

    # parent object for the grid and tile map
    grid_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(50, 50)))
        .add_component(tile_grid.grid)
        .add_component(tile_grid.tile_map)
        .add_component(tile_grid.tile_map_renderer)
        .add_component(RenderLayer(layers.get_layer("Background")))
        .build()
    )

    parent_obj = GameObjectBuilder(Empty).add_component(Transform()).build()
    parent_obj.add_child(grid_obj)

    scene.add_game_object(parent_obj)

    scene.add_game_object(create_camera_game_object(window_settings, layers.get_layer("Default")))

    return scene
