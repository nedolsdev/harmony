"""An input processor modifies the data from a control."""

from __future__ import annotations

from core.packages.input.input_value import InputValue


class InputProcessor[InputValueT: InputValue]:
    """An input processor modifies the data from a control."""

    def process(self, input_value: InputValueT) -> InputValueT:
        """Modify the input value."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
