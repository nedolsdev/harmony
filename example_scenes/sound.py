"""Sound example scene."""

from core.components.transform import Transform
from core.objects.empty import Empty
from core.packages.audio.audio_bus import AudioBus
from core.packages.audio.audio_clip import AudioClip
from core.packages.audio.audio_listener import AudioListener
from core.packages.audio.audio_manager import AudioManager
from core.packages.audio.audio_source import AudioSource
from core.packages.audio.music_player import MusicPlayer
from core.packages.audio.music_track import MusicTrack
from core.packages.audio.play_sound_test import PlaySoundTest
from core.packages.audio.spatializer import AudioSpatializer2D
from core.packages.geometry.vector2 import Vector2
from example_scenes.camera_util import create_camera_game_object
from game.object_builder import GameObjectBuilder
from game.scene import Scene
from game.sorting_layer import SortingLayerManager


def create_sound_test_scene(window_size: int, layers: SortingLayerManager) -> Scene:
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

    scene.add_game_object(create_camera_game_object(window_size, layers.get_layer("Default")))

    return scene
