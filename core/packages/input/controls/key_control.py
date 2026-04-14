"""A control defined as a key on a keyboard."""

from typing import override

from core.packages.input.control import InputControl
from core.packages.input.controls.device import Device, DeviceType
from core.packages.input.controls.devices.keyboard import Keyboard


class KeyControl(InputControl):
    """A control defined as a key on a keyboard."""

    def __init__(self, key: int) -> None:
        """Initialize the KeyControl."""
        super().__init__()
        self.key = key

    @override
    def read_value(self, device: Device) -> bool:
        """Read the value of the input."""
        if device.device_type != DeviceType.KEYBOARD or not isinstance(device, Keyboard):
            msg = "Tried to read KeyControl from non-keyboard device."
            raise ValueError(msg)
        return device.key_state[self.key]
