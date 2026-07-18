"""Sound example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

from example_scenes.helpers.camera_util import create_camera_game_object
from harmony.core.components.transform import Transform
from harmony.core.objects.empty import Empty
from harmony.core.packages.audio.audio_bus import AudioBus
from harmony.core.packages.audio.audio_clip import AudioClip
from harmony.core.packages.audio.audio_listener import AudioListener
from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.core.packages.audio.audio_source import AudioSource
from harmony.core.packages.audio.music_player import MusicPlayer
from harmony.core.packages.audio.music_track import MusicTrack
from harmony.core.packages.audio.play_sound_test import PlaySoundTest
from harmony.core.packages.audio.spatializer import AudioSpatializer2D
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.game.object_builder import GameObjectBuilder
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_sound_test_scene(window_settings: WindowSettings, layers: SortingLayerManager) -> Scene:
    """Return a Scene configured for testing audio playback."""
    scene = Scene()

    sfx_bus = AudioBus("SFX", 1)
    music_bus = AudioBus("Music", 0.5)

    # assets
    clip = AudioClip("./core/packages/audio/example_assets/coin.wav")
    track = MusicTrack("./core/packages/audio/example_assets/music.wav")

    player = MusicPlayer(music_bus)
    player.play(track)

    # listener
    listener_comp = AudioListener()
    listener_obj = GameObjectBuilder(Empty).add_component(Transform()).add_component(listener_comp).build()
    AudioManager().set_listener(listener_comp)
    scene.add_game_object(listener_obj)

    # looping source
    looping_source = AudioSource(clip=clip, bus=sfx_bus, spatializer=AudioSpatializer2D(10, 50))
    looping_source.start_looping()
    AudioManager().register_source(looping_source)

    sfx_obj = (
        GameObjectBuilder(Empty)
        .add_component(Transform(local_position=Vector2(100, 0)))
        .add_component(looping_source)
        .add_component(PlaySoundTest())
        .build()
    )
    scene.add_game_object(sfx_obj)

    scene.add_game_object(create_camera_game_object(window_settings, layers.get_layer("Default")))

    return scene
