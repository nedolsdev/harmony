"""A KeyBinding connects input to one or more keys."""

from core.packages.input.controls.key_control import KeyControl
from core.packages.input.input_action import InputAction
from core.packages.input.input_binding import InputBinding
from core.packages.input.interaction import Interaction
from core.packages.input.processor import InputProcessor


class KeyBinding(InputBinding):
    """A KeyBinding connects input to one or more keys."""

    def __init__(
        self,
        key: int,
        action: InputAction,
        interaction: Interaction,
        *,
        processors: list[InputProcessor] | None = None,
    ) -> None:
        """Initialize the KeyBinding."""
        control = KeyControl(key=key)
        super().__init__(control, action, interaction, processors=processors)
