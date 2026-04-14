"""An InputBinding connects an InputAction to one or many Controls."""

from core.packages.input.control import InputControl
from core.packages.input.controls.device import Device
from core.packages.input.input_action import InputAction
from core.packages.input.interaction import Interaction


class InputBinding:
    """An InputBinding connects an InputAction to one or many Controls."""

    def __init__(
        self,
        control: InputControl,
        action: InputAction,
        interaction: Interaction,
    ) -> None:
        """Initialize the InputBinding."""
        self.control = control
        self.action = action
        self.interaction = interaction

    def update(self, devices: list[Device]) -> None:
        """Update the binding."""
        best_device = self.get_best_device(devices)

        if best_device is None:
            msg = f"Could not find suitable device for input binding '{self}'"
            raise ValueError(msg)

        input_value = self.control.read_value(best_device)
        self.action.value = input_value
        self.interaction.process(self.action, input_value=input_value)

    def get_best_device(self, devices: list[Device]) -> Device | None:
        """Get the best device for the binding from a list of devices."""
        for device in devices:
            if device.device_type == self.control.device_type:
                return device
        return None
