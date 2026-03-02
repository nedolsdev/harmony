"""Audio source component plays and controls an AudioClip."""

import pygame

from core.packages.audio.audio_bus import AudioBus
from core.packages.audio.audio_clip import AudioClip
from core.packages.audio.audio_manager import AudioManager
from game.component import GameComponent


class AudioSource(GameComponent):
    """Audio source component plays and controls an AudioClip."""

    def __init__(self, clip: AudioClip | None, bus: AudioBus | None) -> None:
        """Initialize the AudioSource."""
        self.clip = clip
        self.bus = bus
        self.loop = False
        self.volume = 1.0
        self.channel: pygame.Channel | None = None

    def start_looping(self) -> None:
        """Make the clip loop."""
        self.loop = True

    def stop_looping(self) -> None:
        """Make the clip stop looping."""
        self.loop = False

    def set_volume(self, volume: float) -> None:
        """Set the volume of the clip."""
        self.volume = volume

    def set_channel(self, channel: pygame.Channel) -> None:
        """Set the channel of the AudioSource."""
        self.channel = channel

    def play(self) -> None:
        """Play the AudioSource."""
        AudioManager().play_source(self)

    def stop(self) -> None:
        """Stop the current AudioSource from playing."""
        if self.channel:
            self.channel.stop()
            AudioManager().release_channel(self.channel)
            self.channel = None

    def get_true_volume(self) -> float:
        """Get the true volume of the clip."""
        bus_volume = self.bus.volume if self.bus else 1.0
        master = AudioManager().master_volume
        return self.volume * bus_volume * master

    def apply_volume(self) -> None:
        """Apply the volume to the channel."""
        if self.channel and self.channel.get_busy():
            final = self.get_true_volume()
            self.channel.set_volume(final)

    def update(self) -> None:
        """Update the AudioSource, releasing the channel if needed."""
        if self.channel and not self.channel.get_busy():
            AudioManager().release_channel(self.channel)
            self.channel = None
