"""A KeyBinding connects input to one or more keys."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.input.controls.key_control import KeyControl
from harmony.core.packages.input.input_binding import InputBinding

if TYPE_CHECKING:
    from harmony.core.packages.input.input_action import InputAction
    from harmony.core.packages.input.interaction import Interaction
    from harmony.core.packages.input.processor import InputProcessor


class KeyBinding(InputBinding[float]):
    """A KeyBinding connects input to one or more keys."""

    def __init__(
        self,
        key: int,
        action: InputAction[float],
        interaction: Interaction[float] | None = None,
        *,
        processors: list[InputProcessor[float]] | None = None,
    ) -> None:
        """Initialize the KeyBinding."""
        control = KeyControl(key=key)
        super().__init__(control, action, interaction, processors=processors)
