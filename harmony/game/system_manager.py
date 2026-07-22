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
        self.systems.append(system)

    def pre_init(self) -> None:
        """Before initialization of the system."""
        for system in self.systems:
            system.pre_init()

    def init(self) -> None:
        """Initialize the system."""
        for system in self.systems:
            system.init()

    def pre_update(self) -> None:
        """Update the system."""
        for system in self.systems:
            system.pre_update()

    def update(self) -> None:
        """Update the system."""
        for system in self.systems:
            system.update()

    def fixed_update(self) -> None:
        """Update the system on fixed physics step."""
        for system in self.systems:
            system.fixed_update()

    def late_update(self) -> None:
        """Late update the system."""
        for system in self.systems:
            system.late_update()

    def post_update(self) -> None:
        """Post update the system."""
        for system in self.systems:
            system.post_update()
