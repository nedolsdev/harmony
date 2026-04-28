"""Combines multiple InputBindings into one action."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.input.input_binding import BindingBase

if TYPE_CHECKING:
    from collections.abc import Callable

    from core.packages.input.controls.device import Device
    from core.packages.input.input_action import InputAction, InputValue
    from core.packages.input.input_binding import InputBinding
    from core.packages.input.interaction import Interaction


class CompositeBinding[CompositeValueT: InputValue, PartValueT: InputValue](BindingBase):
    """Combines multiple InputBindings into one action."""

    def __init__(
        self,
        action: InputAction[CompositeValueT],
        interaction: Interaction[CompositeValueT],
        parts: dict[str, InputBinding[PartValueT]],
        compose: Callable[[dict[str, PartValueT]], CompositeValueT],
    ) -> None:
        """Initialize the CompositeBinding."""
        self.action = action
        self.interaction = interaction
        self.parts = parts
        self.compose = compose

    @override
    def update(self, devices: list[Device]) -> None:
        """Update the binding."""
        values: dict[str, PartValueT] = {}

        for name, binding in self.parts.items():
            values[name] = binding.evaluate(devices)

        if not values:
            return

        result = self.compose(values)

        self.action.value = result
        self.interaction.process(self.action, input_value=result)
