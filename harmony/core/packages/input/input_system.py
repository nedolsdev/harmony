"""Input system."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.game.system import System

if TYPE_CHECKING:
    from harmony.core.packages.input.input_manager import InputManager


class InputSystem(System):
    """Input system."""

    def __init__(self, input_manager: InputManager) -> None:
        """Initialize the Input System."""
        super().__init__()
        self.input_manager = input_manager

    def init(self) -> None:
        """Init the system."""
        self.input_manager.device_manager.reset()

    def pre_update(self) -> None:
        """Pre-update the system."""
        self.input_manager.update()

    def post_update(self) -> None:
        """Post-update the system."""
        self.input_manager.post_update()
