"""Default interaction: fires based on value changes."""

from typing import override

from core.packages.input.input_action import InputAction
from core.packages.input.input_value import InputValue
from core.packages.input.interaction import Interaction


class DefaultInteraction[InputValueT: InputValue](Interaction[InputValueT]):
    """Default interaction: fires based on value changes."""

    def __init__(self) -> None:
        """Initialise the DefaultInteraction."""
        self._is_actuated: bool = False

    def _is_non_zero(self, value: InputValueT) -> bool:
        """Determine if input is actuated."""
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, tuple):
            return any(v != 0 for v in value)
        msg = "Invalid type of interaction value."
        raise TypeError(msg)

    @override
    def process(self, action: InputAction[InputValueT], *, input_value: InputValueT) -> None:
        is_actuated: bool = self._is_non_zero(input_value)

        if is_actuated:
            if not self._is_actuated:
                action.start()
            action.perform()

        elif self._is_actuated:
            action.cancel()

        self._is_actuated = is_actuated
