"""Music player component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.core.packages.audio.volume import check_volume
from harmony.game.component import GameComponent

if TYPE_CHECKING:
    from harmony.core.packages.audio.audio_bus import AudioBus
    from harmony.core.packages.audio.music_track import MusicTrack
    from harmony.game.event_handler import EventHandler


class MusicPlayer(GameComponent):
    """Music player component."""

    def __init__(self, bus: AudioBus | None = None) -> None:
        """Initialize the MusicPlayer."""
        self.current_track = None
        self.bus = bus
        self.loop = True
        self._volume = 1.0
        self._paused = False

    @property
    def volume(self) -> float:
        """Volume of the music player."""
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        check_volume(value)
        self._volume = value
        self.apply_volume()

    def get_true_volume(self) -> float:
        """Get the true volume of the track."""
        bus_volume = self.bus.volume if self.bus else 1.0
        master = AudioManager().master_volume
        return self._volume * bus_volume * master

    def apply_volume(self) -> None:
        """Update the volume of the track."""
        pygame.mixer.music.set_volume(self.get_true_volume())

    def play(self, track: MusicTrack, fade_ms: int = 0) -> None:
        """Play a given MusicTrack."""
        if self.current_track == track:
            return

        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)

        pygame.mixer.music.load(track.path)

        loops = -1 if self.loop else 0
        pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)

        self.current_track = track
        self._paused = False
        self.apply_volume()

    def stop(self, fade_ms: int = 0) -> None:
        """Stop the music track."""
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()

        self.current_track = None

    def pause(self) -> None:
        """Pause the track."""
        pygame.mixer.music.pause()
        self._paused = True

    def resume(self) -> None:
        """Resume the track."""
        pygame.mixer.music.unpause()
        self._paused = False

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def late_update(self) -> None:
        """Late update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def fixed_update(self) -> None:
        """Update the component in the physics / fixed loop."""

    @override
    def copy(self) -> MusicPlayer:
        """Copy the component."""
        return MusicPlayer(self.bus)
