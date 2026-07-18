"""Tile map example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.components.render_layer import RenderLayer
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.geometry.vector2 import Vector2
from core.packages.spritesheet.sprite_sheet import SimpleSpriteSheet
from example_scenes.helpers.camera_util import create_camera_game_object
from example_scenes.helpers.test_sprite_sheet import get_sprite_sheet_grid
from game.object_builder import GameObjectBuilder
from game.scene import Scene

if TYPE_CHECKING:
    from game.sorting_layer import SortingLayerManager


def create_sprite_sheet_scene(window_size: int, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing the sprite sheet."""
    scene = Scene()

    sprite_sheet = SimpleSpriteSheet(
        "./core/packages/spritesheet/example_assets/tilemap_packed.png",
        16,
        16,
        grid_gap=0,
    )

    tile_grid = get_sprite_sheet_grid(sprite_sheet, cell_size=16)

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

    scene.add_game_object(create_camera_game_object(window_size, layers.get_layer("Default")))

    return scene
