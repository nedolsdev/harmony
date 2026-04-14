"""An interaction is a specific input pattern."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from core.packages.input.input_action import InputAction


class Interaction[InputValueT: InputValue]:
    """An interaction is a specific input pattern."""

    @abstractmethod
    def process(self, action: InputAction, *, input_value: InputValueT) -> None:
        """Process input action."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
