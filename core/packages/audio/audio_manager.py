"""Audio manager tracks AudioSources and the AudioListener."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

from core.packages.audio.volume import check_volume
from core.packages.timing.delta_time import Singleton
from game.error import DataAlreadyExistsError

if TYPE_CHECKING:
    from core.packages.audio.audio_bus import AudioBus
    from core.packages.audio.audio_clip import AudioClip
    from core.packages.audio.audio_listener import AudioListener
    from core.packages.audio.audio_source import AudioSource


class ChannelStealingPolicy(ABC):
    """Defines a channel stealing policy for the AudioManager."""

    @abstractmethod
    def get_channel(self, channel_sources: dict[pygame.Channel, AudioSource]) -> pygame.Channel | None:
        """Get the channel that should be stolen. Return 'None' if there is no suitable channel to steal."""


class StealFirstNonLoopingSource(ChannelStealingPolicy):
    """Channel stealing policy that steals first non-looping AudioSource."""

    def get_channel(self, channel_sources: dict[pygame.Channel, AudioSource]) -> pygame.Channel | None:
        """Get the channel that should be stolen. Return 'None' if there is no suitable channel to steal."""
        for channel, source in channel_sources.items():
            if not source.loop:
                channel.stop()
                return channel

        return None


class AudioManager(metaclass=Singleton):
    """Audio manager tracks AudioSources and the AudioListener."""

    def __init__(
        self,
        number_of_channels: int = 32,
        master_volume: float = 1,
        stealing_policy: ChannelStealingPolicy = StealFirstNonLoopingSource(),  # noqa: B008 (this is ok because it is a singleton)
    ) -> None:
        """Initialize the AudioManager with a number of channels and default volume."""
        pygame.mixer.set_num_channels(number_of_channels)

        self.master_volume = master_volume
        self.number_of_channels = number_of_channels

        self.sources: list[AudioSource] = []
        self.channels: list[pygame.Channel] = []
        self.buses: list[AudioBus] = []
        self.channel_map: dict[pygame.Channel, AudioSource] = {}

        self.stealing_policy = stealing_policy

        self.active_listener: None | AudioListener = None

    def register_source(self, source: AudioSource) -> None:
        """Register the AudioSource."""
        if source in self.sources:
            msg = "Source is already added."
            raise DataAlreadyExistsError(msg)

        self.sources.append(source)

    def unregister_source(self, source: AudioSource) -> None:
        """Unregister the AudioSource."""
        if source not in self.sources:
            msg = "Could not find AudioSource to remove."
            raise LookupError(msg)

        self.sources.remove(source)

    def register_bus(self, bus: AudioBus) -> None:
        """Register the AudioBus."""
        if bus in self.buses:
            msg = f"AudioBus already registered. ({bus})"
            raise DataAlreadyExistsError(msg)

        self.buses.append(bus)

    def request_channel(self, source: AudioSource) -> pygame.Channel | None:
        """Request a channel for an AudioSource."""
        channel = pygame.mixer.find_channel()

        # no available channel, we need to steal one
        if not channel:
            channel = self.stealing_policy.get_channel(self.channel_map)

        # we couldn't find a suitable channel to steal
        if not channel:
            return None

        self.channel_map[channel] = source
        return channel

    def release_channel(self, channel: pygame.Channel) -> None:
        """Release an Audio Channel."""
        if channel in self.channel_map:
            del self.channel_map[channel]

    def play_source(self, source: AudioSource) -> None:
        """Play a given AudioSource."""
        if not source.clip:
            return

        if source.channel and source.channel.get_busy():
            source.stop()

        channel = self.request_channel(source)
        if not channel:
            return

        loops = -1 if source.loop else 0
        channel.play(source.clip.sound, loops=loops)

        source.channel = channel
        source.apply_volume()

    def play_one_shot(self, clip: AudioClip, volume: float = 1.0, bus: AudioBus | None = None) -> None:
        """Play a given AudioClip as a one-shot sound from any free channel (never steals)."""
        channel = pygame.mixer.find_channel()

        # no free channel, so we can't play it (no stealing here)
        if not channel:
            return

        final = volume
        if bus:
            final *= bus.volume
        final *= self.master_volume

        channel.set_volume(final)
        channel.play(clip.sound)

    def set_master_volume(self, volume: float) -> None:
        """Set the master volume."""
        check_volume(volume)

        self.master_volume = volume
        for source in self.sources:
            source.apply_volume()

    def update(self) -> None:
        """Update the AudioSources."""
        for source in self.sources:
            source.update_source()

        # clean dead (unused) channels
        dead_channels = []
        for channel in self.channel_map:
            if not channel.get_busy():
                dead_channels.append(channel)  # noqa: PERF401

        for channel in dead_channels:
            self.release_channel(channel)

    def set_listener(self, listener: AudioListener) -> None:
        """Set the AudioListener."""
        self.active_listener = listener
