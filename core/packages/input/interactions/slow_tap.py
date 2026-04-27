"""A slow tap interaction."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, override

from core.packages.input.interaction import Interaction

if TYPE_CHECKING:
    from core.packages.input.input_action import InputAction


class SlowTapInteraction(Interaction[float]):
    """A slow tap interaction."""

    def __init__(
        self,
        press_point: float = 0.5,
        duration: float = 0.5,
    ) -> None:
        """Initialize the SlowTapInteraction."""
        super().__init__()
        self.press_point: float = press_point
        self.duration: float = duration

        self._was_pressed: bool = False
        self._press_time: float | None = None

    @override
    def process(self, action: InputAction, *, input_value: float) -> None:
        """Process input action."""
        is_pressed: bool = input_value >= self.press_point
        now: float = time.monotonic()

        # pressed
        if is_pressed and not self._was_pressed:
            self._press_time = now
            action.start()

        # released
        elif not is_pressed and self._was_pressed:
            if self._press_time is not None:
                held_time: float = now - self._press_time

                if held_time >= self.duration:
                    action.perform()
                else:
                    action.cancel()

            self._press_time = None

        self._was_pressed = is_pressed
