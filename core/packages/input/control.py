"""The reference to the actual control input."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from core.packages.input.controls.device import Device, DeviceType


class InputControl[InputValueT: InputValue](ABC):
    """The reference to the actual control input."""

    def __init__(self, device_type: DeviceType) -> None:
        """Initialize the InputControl."""
        self.device_type = device_type

    @abstractmethod
    def read_value(self, device: Device) -> InputValueT:
        """Read the value of the input."""
