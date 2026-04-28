"""The central controller for the input system."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.input.action_map import ActionMap

if TYPE_CHECKING:
    from core.packages.input.device_manager import DeviceManager


class InputSystem:
    """The central controller for the input system."""

    def __init__(self) -> None:
        """Initialize the InputSystem."""
        self.maps: dict[str, ActionMap] = {}

    def update(self, device_manager: DeviceManager) -> None:
        """Update the input system given a list of connected devices."""
        device_manager.update()

        for action_map in self.maps.values():
            if not action_map.active:
                continue

            for binding in action_map.bindings:
                binding.update(device_manager.devices)

    def late_update(self) -> None:
        """Late update the input system, resetting the actions."""
        for action_map in self.maps.values():
            for action in action_map.actions.values():
                action.reset()

    def create_map(self, name: str, *, action_map: ActionMap | None = None) -> ActionMap:
        """Create an action map with a given name."""
        action_map = action_map or ActionMap()
        self.maps[name] = action_map
        return action_map
