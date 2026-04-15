"""Create the game runner for the evolution game."""

from __future__ import annotations

import pygame

from core.packages.audio.audio_manager import AudioManager
from core.packages.input.input_system import InputSystem
from evolution_game.scenes.main_scene import create_main_scene
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.lazy_scene import SimpleLazyScene
from game.logging import EngineLogger
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene_manager import SceneManager


def create_evolution_game() -> Runner:
    """Create the game runner for the evolution game."""
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    event_handler = EventHandler()

    renderer = RenderPipeline(
        title="Evolution Game",
        window_width=1280,
        window_height=720,
        fullscreen=False,
    )

    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    input_system = InputSystem()

    scene_manager = SceneManager()

    scenes = [
        SimpleLazyScene("Main Scene", lambda: create_main_scene(renderer.get_screen_size(), renderer.sorting_layers)),
    ]

    for scene in scenes:
        scene_manager.add_scene(scene)

    game = Runner(renderer, event_handler, scene_manager, input_system)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    return game
