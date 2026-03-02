"""Audio bus component controls the mixing of different sounds."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.audio.audio_manager import AudioManager
from core.packages.audio.volume import check_volume

if TYPE_CHECKING:
    from core.packages.audio.audio_source import AudioSource


class AudioBus:
    """Audio bus component controls the mixing of different sounds."""

    def __init__(self, name: str, volume: float = 1.0) -> None:
        """Initialize the AudioBus with a name and volume."""
        check_volume(volume)

        self.name = name
        self._volume = volume
        self.sources: list[AudioSource] = []

        AudioManager().register_bus(self)

    @property
    def volume(self) -> float:
        """Volume of the AudioBus."""
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        check_volume(value)

        self._volume = value
        for source in self.sources:
            source.apply_volume()

    def add_source(self, source: AudioSource) -> None:
        """Add an AudioSource to the bus."""
        if source not in self.sources:
            self.sources.append(source)

    def remove_source(self, source: AudioSource) -> None:
        """Remove an AudioSource from the bus."""
        if source in self.sources:
            self.sources.remove(source)
