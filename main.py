"""Main entry point for the Agent World game."""

import pygame
from rich.traceback import install

from agent_world.animations.test_animation import test_controller
from agent_world.components.rotate_around import RotateAround
from agent_world.objects.agent import Agent
from agent_world.objects.test_tile_map import grid, tile_map, tile_map_renderer
from core.assets.polygon_asset import PolygonAsset
from core.components.line_2d import Line2D
from core.components.poly_render_2d import PolyRender2D
from core.components.render_layer import RenderLayer
from core.components.sprite_2d import Sprite2D
from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.animation.animator import Animator
from core.packages.audio.audio_bus import AudioBus
from core.packages.audio.audio_clip import AudioClip
from core.packages.audio.audio_listener import AudioListener
from core.packages.audio.audio_manager import AudioManager
from core.packages.audio.audio_source import AudioSource
from core.packages.audio.music_player import MusicPlayer
from core.packages.audio.music_track import MusicTrack
from core.packages.audio.play_sound_test import PlaySoundTest
from core.packages.audio.spatializer import AudioSpatializer2D
from core.packages.camera.camera_component import Camera, Viewport
from core.packages.camera.camera_controller import CameraController
from core.packages.collision.collider_rect import ColliderRect
from core.packages.collision.collision_grouper import CollisionGrouper
from core.packages.collision.collision_layer import CollisionLayer
from core.packages.collision.collision_rule import CollisionRule
from core.packages.collision.collision_test import CollisionTest
from core.packages.geometry.rectangle import Rectangle
from core.packages.geometry.vector2 import Vector2
from core.packages.timing.timer import ComponentUsingTimer
from example_scenes.sound import create_sound_test_scene
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene import Scene
from game.scene_manager import SceneManager

install()


def main() -> None:  # noqa: PLR0915
    """Initialize the game and start the renderer."""
    # init pygame and mixer
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    sfx_bus = AudioBus("SFX", 0)
    music_bus = AudioBus("Music", 0.1)

    clip = AudioClip("./core/packages/audio/example_assets/coin.wav")

    track = MusicTrack("./core/packages/audio/example_assets/music.wav")

    player = MusicPlayer(music_bus)
    player.play(track)

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

    game = Runner(renderer, event_handler, create_sound_test_scene(window_size, renderer.sorting_layers))

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
