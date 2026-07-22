"""Audio source component plays and controls an AudioClip."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.components.transform import Transform
from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.game.behavior import Behavior
from harmony.game.error import MissingComponentDependencyError

if TYPE_CHECKING:
    import pygame

    from harmony.core.packages.audio.audio_bus import AudioBus
    from harmony.core.packages.audio.audio_clip import AudioClip
    from harmony.core.packages.audio.spatializer import AudioSpatializer2D


class AudioSource(Behavior):
    """Audio source component plays and controls an AudioClip."""

    transform: Transform

    def __init__(
        self,
        clip: AudioClip | None,
        bus: AudioBus | None,
        *,
        spatializer: AudioSpatializer2D | None = None,
    ) -> None:
        """Initialize the AudioSource."""
        super().__init__()
        self.clip = clip
        self.bus = bus
        self.loop = False
        self.volume = 1.0
        self.channel: pygame.Channel | None = None

        self.spatializer = spatializer

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        if self.spatializer is not None and not self.game_object.has_component(Transform):
            msg = "Spatial AudioSource does not have necessary 'Transform' component attached."
            raise MissingComponentDependencyError(msg)

        self.transform = self.game_object.get_component(Transform)

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
            base_volume = self.get_true_volume()

            listener = AudioManager().active_listener

            if self.spatializer is not None and listener is not None:
                left, right = self.spatializer.calculate(
                    self.transform.world_position,
                    listener.transform.world_position,
                )

                left *= base_volume
                right *= base_volume

                self.channel.set_volume(left, right)
            else:
                self.channel.set_volume(base_volume)

    def update_source(self) -> None:
        """Update the AudioSource, releasing the channel if needed."""
        if self.channel:
            if self.channel.get_busy():
                self.apply_volume()
            else:
                AudioManager().release_channel(self.channel)
                self.channel = None

    @override
    def copy(self) -> AudioSource:
        """Copy the component."""
        return AudioSource(self.clip, self.bus, spatializer=self.spatializer)
