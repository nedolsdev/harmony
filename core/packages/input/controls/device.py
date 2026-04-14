"""A device that can record inputs."""
from __future__ import annotations

from enum import Enum, auto

from core.packages.input.control import InputControl


class DeviceType(Enum):
    """A type of device."""

    KEYBOARD = auto()
    MOUSE = auto()


class Device(InputControl):
    """A device that can record inputs."""

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize the Device."""
        self.device_type = device_type

    def update(self) -> None:
        """Update the device state."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
