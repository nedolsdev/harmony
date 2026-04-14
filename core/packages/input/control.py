"""The reference to the actual control input."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.input.controls.device import Device, DeviceType


class InputControl:
    """The reference to the actual control input."""

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize the InputControl."""
        self.device_type = device_type

    def read_value(self, device: Device) -> float:
        """Read the value of the input."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
