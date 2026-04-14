"""An action map defines a set of related input actions."""

from core.packages.input.input_action import InputAction


class ActionMap:
    """An action map defines a set of related input actions."""

    def __init__(self) -> None:
        """Initialize the ActionMap."""
        self.actions: dict[str, InputAction] = {}

    def create_action(self, name: str) -> InputAction:
        """Create an InputAction for a given name."""
        input_action = InputAction(name)
        self.actions[input_action.name] = input_action
        return input_action
