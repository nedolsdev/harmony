"""An action map defines a set of related input actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.input.input_action import InputAction

if TYPE_CHECKING:
    from core.packages.input.input_binding import BindingBase


class ActionMap:
    """An action map defines a set of related input actions."""

    def __init__(self) -> None:
        """Initialize the ActionMap."""
        self.actions: dict[str, InputAction] = {}
        self.bindings: list[BindingBase] = []
        self.active = True

    def add_action(self, name: str) -> InputAction:
        """Create an InputAction for a given name."""
        input_action = InputAction(name)
        self.actions[input_action.name] = input_action
        return input_action

    def add_binding(self, binding: BindingBase) -> None:
        """Add a binding to the ActionMap."""
        self.bindings.append(binding)

    def activate(self) -> None:
        """Set the ActionMap as active."""
        self.active = True

    def deactivate(self) -> None:
        """Set the ActionMap as inactive."""
        self.active = False
