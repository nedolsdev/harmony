"""An input processor modifies the data from a control."""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.packages.input.input_value import InputValue


class InputProcessor[InputValueT: InputValue](ABC):
    """An input processor modifies the data from a control."""

    @abstractmethod
    def process(self, input_value: InputValueT) -> InputValueT:
        """Modify the input value."""
