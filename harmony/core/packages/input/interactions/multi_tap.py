"""A multi-tap interaction."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, override

from harmony.core.packages.input.interaction import Interaction

if TYPE_CHECKING:
    from harmony.core.packages.input.input_action import InputAction


class MultiTapInteraction(Interaction[float]):
    """A multi-tap interaction."""

    def __init__(
        self,
        tap_time: float = 0.2,
        tap_delay: float | None = None,
        tap_count: int = 2,
        press_point: float = 0.5,
    ) -> None:
        """Initialize the MultiTapInteraction."""
        super().__init__()

        self.tap_time: float = tap_time
        self.tap_delay: float = tap_delay if tap_delay is not None else 2.0 * tap_time
        self.tap_count: int = tap_count
        self.press_point: float = press_point

        self._was_pressed: bool = False

        self._press_start: float | None = None
        self._last_release: float | None = None

        self._completed_taps: int = 0
        self._waiting_for_release: bool = False

    def _reset(self) -> None:
        """Reset interaction state."""
        self._press_start = None
        self._last_release = None
        self._completed_taps = 0
        self._waiting_for_release = False
        self._was_pressed = False

    @override
    def process(self, action: InputAction, *, input_value: float) -> None:
        """Process input action."""
        now: float = time.monotonic()
        is_pressed: bool = input_value >= self.press_point

        # start
        if is_pressed and not self._was_pressed:
            # delay violation: too much time between taps
            if self._last_release is not None and (now - self._last_release) > self.tap_delay:
                action.cancel()
                self._reset()
                return

            self._press_start = now
            self._waiting_for_release = True

            if self._completed_taps == 0:
                action.start()

        # released
        elif not is_pressed and self._was_pressed:
            if self._press_start is not None:
                held_time: float = now - self._press_start

                # too long press
                if held_time >= self.tap_time:
                    action.cancel()
                    self._reset()
                    return

            if self._waiting_for_release:
                self._completed_taps += 1
                self._last_release = now
                self._waiting_for_release = False

                if self._completed_taps >= self.tap_count:
                    action.perform()
                    self._reset()

        self._was_pressed = is_pressed
