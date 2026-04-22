"""Main entry point for the Agent World game."""

from __future__ import annotations

import pygame
from rich.traceback import install

from core.packages.audio.audio_manager import AudioManager
from core.packages.input.input_system import InputSystem
from example_scenes.animation import create_animation_scene
from example_scenes.collision import create_collision_scene
from example_scenes.input import create_input_scene
from example_scenes.physics import create_physics_scene
from example_scenes.physics_collision import create_physics_collision_scene
from example_scenes.rotation import create_rotation_scene
from example_scenes.sound import create_sound_test_scene
from example_scenes.tile_map import create_tile_map_scene
from example_scenes.timer import create_timer_scene
from example_scenes.ui import create_ui_scene
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.lazy_scene import SimpleLazyScene
from game.logging import EngineLogger
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene_manager import SceneManager

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    # init pygame and mixer
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    event_handler = EventHandler()

    grid_size = 12
    tile_size = 60
    window_size = grid_size * tile_size

    renderer = RenderPipeline(title="Agent World", window_width=window_size, window_height=window_size)
    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    input_system = InputSystem()

    scene_manager = SceneManager()
    game = Runner(renderer, event_handler, scene_manager, input_system)

    collision_manager = game.physics.collision_manager

    scenes = [
        SimpleLazyScene(
            "Animation Scene",
            lambda: create_animation_scene(window_size, renderer.sorting_layers),
        ),
        SimpleLazyScene(
            "Physics Collision Scene",
            lambda: create_physics_collision_scene(window_size, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Physics Scene", lambda: create_physics_scene(window_size, renderer.sorting_layers)),
        SimpleLazyScene("Input Scene", lambda: create_input_scene(window_size, renderer.sorting_layers, input_system)),
        SimpleLazyScene("UI Scene", lambda: create_ui_scene(window_size, renderer.sorting_layers)),
        SimpleLazyScene(
            "Collision Scene",
            lambda: create_collision_scene(window_size, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Timer Scene", lambda: create_timer_scene(window_size, renderer.sorting_layers)),
        SimpleLazyScene("Sound Scene", lambda: create_sound_test_scene(window_size, renderer.sorting_layers)),
        SimpleLazyScene("Rotation Scene", lambda: create_rotation_scene(window_size, renderer.sorting_layers)),
        SimpleLazyScene("Tile Map Scene", lambda: create_tile_map_scene(window_size, renderer.sorting_layers)),
    ]

    for scene in scenes:
        scene_manager.add_scene(scene)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
