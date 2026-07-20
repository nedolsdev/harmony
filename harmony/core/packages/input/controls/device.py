"""A device that can record inputs."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.core.packages.input.input_backend import InputBackend


class DeviceType(Enum):
    """A type of device."""

    KEYBOARD = auto()
    MOUSE = auto()


class Device(ABC):
    """A device that can record inputs."""

    def __init__(self, device_type: DeviceType, input_backend: InputBackend) -> None:
        """Initialize the Device."""
        self.device_type = device_type
        self.input_backend = input_backend

    def update_backend(self) -> None:
        """Update the device state."""
        self.input_backend.update()

    @abstractmethod
    def update(self) -> None:
        """Update the device."""
