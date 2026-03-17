"""Main entry point for the Agent World game."""

import pygame
from rich.traceback import install

from core.packages.audio.audio_manager import AudioManager
from example_scenes.collision import create_collision_scene
from example_scenes.rotation import create_rotation_scene
from example_scenes.sound import create_sound_test_scene
from example_scenes.tile_map import create_tile_map_scene
from example_scenes.timer import create_timer_scene
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene import Scene
from game.scene_manager import SceneManager

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    # init pygame and mixer
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    scene_manager = SceneManager()

    scene = Scene("Main Scene")

    scene_manager.add_scene(scene)
    scene_manager.set_active_scene("Main Scene")

    event_handler = EventHandler()

    grid_size = 12
    tile_size = 60
    window_size = grid_size * tile_size

    renderer = RenderPipeline(title="Agent World", window_width=window_size, window_height=window_size)
    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    game = Runner(renderer, event_handler, create_collision_scene(window_size, renderer.sorting_layers))

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
