"""Main entry point for the Agent World game."""

from __future__ import annotations

from rich.traceback import install

from example_scenes.animation import create_animation_scene
from example_scenes.collision import create_collision_scene
from example_scenes.input import create_input_scene
from example_scenes.physics import create_physics_scene
from example_scenes.physics_collision import create_physics_collision_scene
from example_scenes.rotation import create_rotation_scene
from example_scenes.sound import create_sound_test_scene
from example_scenes.sprite_sheet import create_sprite_sheet_scene
from example_scenes.tile_map import create_tile_map_scene
from example_scenes.timer import create_timer_scene
from example_scenes.ui import create_ui_scene
from harmony.core.simple_runner import SimpleRunner
from harmony.game.lazy_scene import SimpleLazyScene
from harmony.game.window import DisplayMode, WindowSettings

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    settings = WindowSettings(mode=DisplayMode.WINDOWED, world_resolution=(750, 750), window_size=(750, 750))

    game = SimpleRunner(settings)

    renderer = game.renderer

    scene_manager = game.scene_manager

    scenes = [
        SimpleLazyScene(
            "Physics Collision Scene",
            lambda: create_physics_collision_scene(settings, renderer.sorting_layers, game.physics.collision_manager),
        ),
        SimpleLazyScene("UI Scene", lambda: create_ui_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sprite Sheet Scene", lambda: create_sprite_sheet_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Tile Map Scene", lambda: create_tile_map_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene(
            "Animation Scene",
            lambda: create_animation_scene(settings, renderer.sorting_layers),
        ),
        SimpleLazyScene("Physics Scene", lambda: create_physics_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene(
            "Input Scene",
            lambda: create_input_scene(settings, renderer.sorting_layers, game.input_system.input_manager),
        ),
        SimpleLazyScene(
            "Collision Scene",
            lambda: create_collision_scene(settings, renderer.sorting_layers, game.physics.collision_manager),
        ),
        SimpleLazyScene("Timer Scene", lambda: create_timer_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sound Scene", lambda: create_sound_test_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Rotation Scene", lambda: create_rotation_scene(settings, renderer.sorting_layers)),
    ]

    for scene in scenes:
        scene_manager.add_scene(scene)

    game.start()


if __name__ == "__main__":
    main()
