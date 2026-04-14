"""The reference to the actual control input."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from core.packages.input.controls.device import Device, DeviceType


class InputControl[InputValueT: InputValue]:
    """The reference to the actual control input."""

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize the InputControl."""
        self.device_type = device_type

    def read_value(self, device: Device) -> InputValueT:
        """Read the value of the input."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
