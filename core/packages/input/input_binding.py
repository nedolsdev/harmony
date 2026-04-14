"""An InputBinding connects an InputAction to one or many Controls."""
from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from core.packages.input.control import InputControl
    from core.packages.input.controls.device import Device
    from core.packages.input.input_action import InputAction
    from core.packages.input.interaction import Interaction
    from core.packages.input.processor import InputProcessor


class InputBinding[InputValueT: InputValue]:
    """An InputBinding connects an InputAction to one or many Controls."""

    def __init__(
        self,
        control: InputControl[InputValueT],
        action: InputAction[InputValueT],
        interaction: Interaction[InputValueT],
        *,
        processors: list[InputProcessor[InputValueT]] | None = None,
    ) -> None:
        """Initialize the InputBinding."""
        self.control = control
        self.action = action
        self.interaction = interaction

        self.processors = processors or []

    def update(self, devices: list[Device]) -> None:
        """Update the binding."""
        best_device = self.get_best_device(devices)

        if best_device is None:
            msg = f"Could not find suitable device for input binding '{self}'"
            raise ValueError(msg)

        raw_value = self.control.read_value(best_device)

        input_value = raw_value

        for processor in self.processors:
            input_value = processor.process(input_value)

        self.action.value = input_value
        self.interaction.process(self.action, input_value=input_value)

    def get_best_device(self, devices: list[Device]) -> Device | None:
        """Get the best device for the binding from a list of devices."""
        for device in devices:
            if device.device_type == self.control.device_type:
                return device
        return None
