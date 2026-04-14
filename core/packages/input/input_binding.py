"""An InputBinding connects an InputAction to one or many Controls."""

from core.packages.input.control import InputControl
from core.packages.input.input_action import InputAction
from core.packages.input.interaction import Interaction


class InputBinding:
    """An InputBinding connects an InputAction to one or many Controls."""

    def __init__(
        self,
        control: InputControl,
        action: InputAction,
        interaction: Interaction,
    ) -> None:
        """Initialize the InputBinding."""
        self.control = control
        self.action = action
        self.interaction = interaction
