"""Main entry point for the Agent World game."""

from __future__ import annotations

import pygame
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
from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.core.packages.input.input_system import InputSystem
from harmony.core.packages.render.render_pipeline import RenderPipeline
from harmony.core.packages.render.resolution import ResolutionManager
from harmony.game.event_handler import EventHandler
from harmony.game.image_cache import ImageCache
from harmony.game.lazy_scene import SimpleLazyScene
from harmony.game.logging import EngineLogger
from harmony.game.runner import Runner
from harmony.game.scene_manager import SceneManager
from harmony.game.window import DisplayMode, WindowSettings

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    # init pygame and mixer
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    event_handler = EventHandler()

    settings = WindowSettings(mode=DisplayMode.WINDOWED, world_resolution=(750, 750), window_size=(750, 750))

    resolution = ResolutionManager()

    renderer = RenderPipeline(resolution, settings)
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
            lambda: create_animation_scene(settings, renderer.sorting_layers),
        ),
        SimpleLazyScene(
            "Physics Collision Scene",
            lambda: create_physics_collision_scene(settings, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Physics Scene", lambda: create_physics_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sprite Sheet Scene", lambda: create_sprite_sheet_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Input Scene", lambda: create_input_scene(settings, renderer.sorting_layers, input_system)),
        SimpleLazyScene("UI Scene", lambda: create_ui_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene(
            "Collision Scene",
            lambda: create_collision_scene(settings, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Timer Scene", lambda: create_timer_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sound Scene", lambda: create_sound_test_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Rotation Scene", lambda: create_rotation_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Tile Map Scene", lambda: create_tile_map_scene(settings, renderer.sorting_layers)),
    ]

    for scene in scenes:
        scene_manager.add_scene(scene)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
