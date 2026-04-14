"""Some MouseBindings that connects an InputAction to inputs on a mouse."""

from core.packages.input.controls.mouse_control import MouseClickControl
from core.packages.input.input_action import InputAction
from core.packages.input.input_binding import InputBinding
from core.packages.input.interaction import Interaction
from core.packages.input.processor import InputProcessor


class MouseClickBinding(InputBinding[float]):
    """A MouseClickBinding connects a button click to an input action."""

    def __init__(
        self,
        button_key: int,
        action: InputAction[float],
        interaction: Interaction[float],
        *,
        processors: list[InputProcessor[float]] | None = None,
    ) -> None:
        """Initialize the MouseClickBinding."""
        control = MouseClickControl(key=button_key)
        super().__init__(control, action, interaction, processors=processors)
