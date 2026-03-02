"""Play sound on start test component."""

from typing import override

from core.packages.audio.audio_source import AudioSource
from game.behavior import Behavior
from game.event_handler import EventHandler


class PlaySoundTest(Behavior):
    """Play sound on start test component."""

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""
        source = self.game_object.get_component(AudioSource)
        source.play()

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
