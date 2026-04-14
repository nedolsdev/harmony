"""The reference to the actual input on a keyboard."""

from typing import override

from core.packages.input.control import InputControl
from core.packages.input.controls.device import Device, DeviceType
from core.packages.input.controls.devices.keyboard import Keyboard


class KeyboardInputControl(InputControl):
    """The reference to the actual input on a keyboard."""

    def __init__(self) -> None:
        """Initialize the InputControl."""
        super().__init__(device_type=DeviceType.KEYBOARD)

    @override
    def read_value(self, device: Device) -> float:
        """Read the value of the input."""
        if device.device_type != DeviceType.KEYBOARD or not isinstance(device, Keyboard):
            msg = "Tried to read KeyControl from non-keyboard device."
            raise ValueError(msg)
        return self.read_value_from_keyboard(device)

    def read_value_from_keyboard(self, keyboard: Keyboard) -> float:
        """Read the value of the input from a keyboard."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
