"""An input processor modifies the data from a control."""


class InputProcessor:
    """An input processor modifies the data from a control."""

    def process(self, input_value: float) -> float:
        """Modify the input value."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
