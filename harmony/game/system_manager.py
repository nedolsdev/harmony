"""SystemManager manages the systems within a game scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.game.component_manager import ComponentManager
    from harmony.game.system import System


class SystemManager:
    """SystemManager manages the systems within a game scene."""

    def __init__(self, component_manager: ComponentManager) -> None:
        """Initialize the SystemManager."""
        self.component_manager = component_manager
        self.systems: list[System] = []

    def add_system(self, system: System) -> None:
        """Add a system to the SystemManager."""
        self.system = system
