"""The reference to the actual input from a mouse."""

from typing import override

from core.packages.input.control import InputControl
from core.packages.input.controls.device import Device, DeviceType
from core.packages.input.controls.devices.mouse import Mouse


class MouseInputControl(InputControl):
    """The reference to the actual input from a mouse."""

    def __init__(self) -> None:
        """Initialize the InputControl."""
        super().__init__(device_type=DeviceType.MOUSE)

    @override
    def read_value(self, device: Device) -> float:
        """Read the value of the input."""
        if device.device_type != DeviceType.MOUSE or not isinstance(device, Mouse):
            msg = "Tried to read MouseInputControl from non-mouse device."
            raise ValueError(msg)
        return self.read_value_from_mouse(device)

    def read_value_from_mouse(self, mouse: Mouse) -> float:
        """Read the value of the input from a mouse."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
