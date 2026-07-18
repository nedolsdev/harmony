"""The DeviceDiscoverer finds connected devices."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from harmony.core.packages.input.controls.devices.keyboard import PygameKeyboard
from harmony.core.packages.input.controls.devices.mouse import PygameMouse

if TYPE_CHECKING:
    from harmony.core.packages.input.controls.device import Device
    from harmony.core.packages.input.input_backend import PygameInputBackend


class DeviceDiscoverer(ABC):
    """The DeviceDiscoverer finds connected devices."""

    @abstractmethod
    def discover_devices(self) -> list[Device]:
        """Discover the list of currently connected devices."""


class PygameDeviceDiscoverer(DeviceDiscoverer):
    """Finds devices compatible with Pygame."""

    def __init__(self, pygame_backend: PygameInputBackend) -> None:
        """Initialize the PygameDeviceDiscoverer."""
        self.pygame_backend = pygame_backend

    def discover_devices(self) -> list[Device]:
        """Discover the list of currently connected devices."""
        keyboard = PygameKeyboard(self.pygame_backend)
        mouse = PygameMouse(self.pygame_backend)
        return [keyboard, mouse]
