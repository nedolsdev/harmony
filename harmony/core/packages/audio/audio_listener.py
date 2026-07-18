"""Audio listener component computes the spatial audio of the scene from a given point."""

from __future__ import annotations

from typing import override

from harmony.core.components.transform import Transform
from harmony.game.behavior import Behavior
from harmony.game.error import MissingComponentDependencyError


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
