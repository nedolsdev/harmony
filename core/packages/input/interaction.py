"""An interaction is a specific input pattern."""

from abc import abstractmethod

from core.packages.input.input_action import InputAction
from core.packages.input.input_value import InputValue


class Interaction[InputValueT: InputValue]:
    """An interaction is a specific input pattern."""

    @abstractmethod
    def process(self, action: InputAction, *, input_value: InputValueT) -> None:
        """Process input action."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
