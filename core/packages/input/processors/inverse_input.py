"""A simple input processor that inverts the input."""

from __future__ import annotations

from core.packages.input.processor import InputProcessor


class InverseInput(InputProcessor[tuple[float, ...]]):
    """A simple input processor that inverts the input."""

    def process(self, input_value: tuple[float, ...]) -> tuple[float, ...]:
        """Modify the input value."""

        def convert(value: float) -> float:
            # NOTE: -False is 0 not 1
            if isinstance(value, bool):
                return not value
            return -value

        return tuple(convert(x) for x in input_value)
