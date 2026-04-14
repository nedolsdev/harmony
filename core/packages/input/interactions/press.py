"""A simple press interaction."""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, override

from core.packages.input.interaction import Interaction

if TYPE_CHECKING:
    from core.packages.input.input_action import InputAction


class PressBehavior(Enum):
    """PressBehavior defines when PressInteraction activates."""

    PRESS_ONLY = auto()
    RELEASE_ONLY = auto()
    PRESS_AND_RELEASE = auto()


class PressInteraction(Interaction[float]):
    """A simple press interaction."""

    def __init__(self, press_point: float = 0.5, behavior: PressBehavior = PressBehavior.PRESS_ONLY) -> None:
        """Initialize the PressInteraction."""
        super().__init__()
        self.press_point = press_point
        self.behavior = behavior

        self._was_pressed = False

    @override
    def process(self, action: InputAction, *, input_value: float) -> None:
        """Process input action."""
        is_pressed: bool = input_value >= self.press_point

        if is_pressed and not self._was_pressed:
            # start the action once the button is first pressed
            action.start()

            if self.behavior in (PressBehavior.PRESS_ONLY, PressBehavior.PRESS_AND_RELEASE):
                action.perform()

        elif not is_pressed and self._was_pressed:
            # button has stopping pressed
            if self.behavior in (PressBehavior.RELEASE_ONLY, PressBehavior.PRESS_AND_RELEASE):
                action.perform()

        self._was_pressed = is_pressed
