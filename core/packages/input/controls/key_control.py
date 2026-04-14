"""A control defined as a key on a keyboard."""

from typing import override

from core.packages.input.controls.devices.keyboard import Keyboard
from core.packages.input.controls.keyboard_input import KeyboardInputControl


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
