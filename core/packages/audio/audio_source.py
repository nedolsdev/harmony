"""Audio source component plays and controls an AudioClip."""

from core.packages.audio.audio_clip import AudioClip
from game.component import GameComponent


class AudioSource(GameComponent):
    """Audio source component plays and controls an AudioClip."""

    def __init__(self, clip: AudioClip) -> None:
        """Initialize the AudioSource."""
        self.clip = clip
        self.loop = False
        self.volume = 1.0
        self.channel = None

    def start_looping(self) -> None:
        """Make the clip loop."""
        self.loop = True

    def stop_looping(self) -> None:
        """Make the clip stop looping."""
        self.loop = False

    def set_volume(self, volume: float) -> None:
        """Set the volume of the clip."""
        self.volume = volume
