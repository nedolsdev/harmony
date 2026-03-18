"""Audio listener component computes the spatial audio of the scene from a given point."""

from typing import override

from core.components.transform import Transform
from game.behavior import Behavior
from game.error import MissingComponentDependencyError
from game.event_handler import EventHandler


class AudioListener(Behavior):
    """Audio listener component computes the spatial audio of the scene from a given point."""

    transform: Transform

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        if not self.game_object.has_component(Transform):
            msg = "AudioListener does not have necessary 'Transform' component attached."
            raise MissingComponentDependencyError(msg)

        self.transform = self.game_object.get_component(Transform)

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
