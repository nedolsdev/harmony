"""The central controller for managing inputs."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.core.packages.input.action_map import ActionMap

if TYPE_CHECKING:
    from harmony.core.packages.input.device_manager import DeviceManager


class InputManager:
    """The central controller for managing inputs."""

    def __init__(self, device_manager: DeviceManager) -> None:
        """Initialize the InputManager."""
        self.maps: dict[str, ActionMap] = {}
        self.device_manager = device_manager

    def update(self) -> None:
        """Update the input manager given a list of connected devices."""
        self.device_manager.update()

        for action_map in self.maps.values():
            if not action_map.active:
                continue

            for binding in action_map.bindings:
                binding.update(self.device_manager.devices)

    def post_update(self) -> None:
        """Post update the input manager, resetting the actions."""
        for action_map in self.maps.values():
            for action in action_map.actions.values():
                action.reset()

    def create_map(self, name: str, *, action_map: ActionMap | None = None) -> ActionMap:
        """Create an action map with a given name."""
        action_map = action_map or ActionMap()
        self.maps[name] = action_map
        return action_map
