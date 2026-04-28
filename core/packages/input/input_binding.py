"""An InputBinding connects an InputAction to one or many Controls."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from core.packages.input.control import InputControl
    from core.packages.input.controls.device import Device
    from core.packages.input.input_action import InputAction
    from core.packages.input.interaction import Interaction
    from core.packages.input.processor import InputProcessor


class BindingBase(ABC):
    """A base class for input bindings."""

    @abstractmethod
    def update(self, devices: list[Device]) -> None:
        """Update the binding."""


class InputBinding[InputValueT: InputValue](BindingBase):
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
        self.processors: list[InputProcessor[InputValueT]] = processors or []

    def evaluate(self, devices: list[Device]) -> InputValueT:
        """Compute the processed value for this binding."""
        device = self.get_best_device(devices)

        if device is None:
            msg = f"Could not find suitable device for input binding '{self}'"

            raise ValueError(msg)

        value: InputValueT = self.control.read_value(device)

        for processor in self.processors:
            value = processor.process(value)

        return value

    @override
    def update(self, devices: list[Device]) -> None:
        """Update the binding."""
        input_value = self.evaluate(devices)
        self.action.value = input_value
        self.interaction.process(self.action, input_value=input_value)

    def get_best_device(self, devices: list[Device]) -> Device | None:
        """Get the best device for the binding from a list of devices."""
        for device in devices:
            if device.device_type == self.control.device_type:
                return device
        return None
