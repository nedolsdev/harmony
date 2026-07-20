"""A control defined as a key on a keyboard."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.input.controls.keyboard_input import KeyboardInputControl

if TYPE_CHECKING:
    from harmony.core.packages.input.controls.devices.keyboard import Keyboard


class KeyControl(KeyboardInputControl):
    """A control defined as a key on a keyboard."""

    def __init__(self, key: int) -> None:
        """Initialize the KeyControl."""
        super().__init__()
        self.key = key

    @override
    def read_value_from_keyboard(self, keyboard: Keyboard) -> bool:
        """Read the value of the input."""
        return keyboard.key_state.get(self.key, False)
