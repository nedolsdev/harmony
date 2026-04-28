"""Device manager."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.input.controls.device import Device, DeviceType
    from core.packages.input.device_discoverer import DeviceDiscoverer


class DeviceManager:
    """Device manager."""

    def __init__(self, discoverer: DeviceDiscoverer) -> None:
        """Initialize the DeviceManager."""
        self.devices: list[Device] = []
        self.devices_by_type: dict[DeviceType, list[Device]] = {}
        self.discoverer = discoverer

    def add_device(self, device: Device) -> None:
        """Add a device."""
        self.devices.append(device)
        self.devices_by_type.setdefault(device.device_type, []).append(device)

    def reset(self) -> None:
        """Reset the devices connected to the DeviceManager."""
        self.devices = []
        self.devices_by_type = {}
        devices = self.discover_devices()
        for device in devices:
            self.add_device(device)

    def get_devices_of_type(self, device_type: DeviceType) -> list[Device]:
        """Get a specific device type."""
        return self.devices_by_type.get(device_type, [])

    def update(self) -> None:
        """Update the devices."""
        for device in self.devices:
            device.update_backend()
            device.update()

    def discover_devices(self) -> list[Device]:
        """Discover the list of currently connected devices."""
        return self.discoverer.discover_devices()
