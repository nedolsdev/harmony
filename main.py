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
from core.packages.geometry.rectangle import Rectangle
from core.packages.timing.timer import ComponentUsingTimer
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene import Scene
from game.scene_manager import SceneManager
from game.vector2 import Vector2

install()


def main() -> None:  # noqa: PLR0915
    """Initialize the game and start the renderer."""
    # init pygame and mixer
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    AudioManager(number_of_channels=32)

    sfx_bus = AudioBus("SFX", 0.1)
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

    bg_layer = renderer.sorting_layers.get_layer("Background")
    default_layer = renderer.sorting_layers.get_layer("Default")

    game = Runner(renderer, event_handler, scene)

    empty = GameObjectBuilder(Empty).add_component(Transform(local_position=Vector2(0, 0))).build()

    grid_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(50, 50)))
        .add_component(RenderLayer(bg_layer))
        .add_component(grid)
        .add_component(tile_map)
        .add_component(tile_map_renderer)
        .build()
    )

    empty.add_child(grid_obj)

    scene.add_game_object(empty)

    # line
    line_prefab = (
        GameObjectBuilder(Agent)
        .add_component(Transform(local_scale=Vector2(0.5, 0.5)))
        .add_component(
            Line2D(
                start=Vector2(0, 0),
                end=Vector2(100, 100),
                material=ColorMaterial((0, 255, 0)),
                width=5,
            ),
        )
        .add_component(
            Line2D(
                start=Vector2(0, 0),
                end=Vector2(-100, 100),
                material=ColorMaterial((255, 0, 0)),
                width=5,
            ),
        )
        .add_component(Animator(test_controller))
        .add_component(RenderLayer(default_layer))
        .build_as_prefab()
    )

    empty2 = GameObjectBuilder(Empty).add_component(Transform(local_position=Vector2(250, 250))).build()

    line_object = line_prefab.create_object()

    empty2.add_child(line_object)

    scene.add_game_object(empty2)

    # square
    square = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 0), local_scale=Vector2(4, 4)))
        .add_component(Sprite2D(25, 25, ColorMaterial((255, 0, 0))))
        .add_component(RenderLayer(default_layer))
        .add_component(
            PolyRender2D(
                PolygonAsset(
                    polygon=Rectangle(25, 25, center=Vector2.zero()),
                    outline_color=(0, 255, 0),
                    outline_width=5,
                ),
            ),
        )
        .build()
    )

    rotation_parent = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(400, 400)))
        .add_component(RenderLayer(default_layer))
        .add_component(RotateAround(2))
        .build()
    )

    rotation_parent.add_child(square)

    scene.add_game_object(rotation_parent)

    camera = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_scale=Vector2(1, 1)))
        .add_component(
            Camera(
                Viewport(
                    window_size,
                    window_size,
                ),
            ),
        )
        .add_component(RenderLayer(default_layer))
        .add_component(CameraController(speed=50))
        .build()
    )

    scene.add_game_object(camera)

    # naive timer
    timer_example = (
        GameObjectBuilder(Empty)
        .add_component(Transform())
        .add_component(ComponentUsingTimer())
        .add_component(RenderLayer(default_layer))
        .build()
    )

    scene.add_game_object(timer_example)

    # listener
    listener_comp = AudioListener()

    listener_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(0, 0)))
        .add_component(listener_comp)
        .add_component(RenderLayer(default_layer))
        .build()
    )

    AudioManager().set_listener(listener_comp)

    scene.add_game_object(listener_obj)

    # local audio source
    looping_source = AudioSource(clip=clip, bus=sfx_bus, spatializer=AudioSpatializer2D(10, 50))
    looping_source.start_looping()

    AudioManager().register_source(looping_source)

    audio_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 0)))
        .add_component(looping_source)
        .add_component(RenderLayer(default_layer))
        .add_component(PlaySoundTest())
        .build()
    )

    scene.add_game_object(audio_obj)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
