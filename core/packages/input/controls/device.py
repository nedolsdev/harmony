"""A device that can record inputs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import override

from core.packages.input.control import InputControl


class DeviceType(Enum):
    """A type of device."""

    KEYBOARD = auto()
    MOUSE = auto()


class Device(InputControl, ABC):
    """A device that can record inputs."""

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize the Device."""
        self.device_type = device_type

    @abstractmethod
    def update(self) -> None:
        """Update the device state."""

    @override
    def read_value(self, device: Device) -> None:
        """Read the value of the input."""
