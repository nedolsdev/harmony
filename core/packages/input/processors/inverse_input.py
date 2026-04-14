"""A simple input processor that inverts the input."""

from core.packages.input.processor import InputProcessor


class InverseInput(InputProcessor):
    """A simple input processor that inverts the input."""

    def process(self, input_value: float) -> float:
        """Modify the input value."""
        # NOTE: -False is 0 not 1
        if isinstance(input_value, bool):
            return not input_value
        return -input_value
