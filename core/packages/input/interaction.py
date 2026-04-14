"""An interaction is a specific input pattern."""

from abc import abstractmethod

from core.packages.input.input_action import InputAction


class Interaction:
    """An interaction is a specific input pattern."""

    @abstractmethod
    def process(self, action: InputAction, *, input_value: float) -> None:
        """Process input action."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
