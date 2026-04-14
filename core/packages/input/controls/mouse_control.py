"""Some different mouse controls."""

from typing import override

from core.packages.input.controls.devices.mouse import Mouse
from core.packages.input.controls.mouse_input import MouseInputControl


class MouseClickControl(MouseInputControl):
    """A control defined as the click of a mouse."""

    def __init__(self, key: int) -> None:
        """Initialize the MouseClickControl."""
        super().__init__()
        self.key = key

    @override
    def read_value_from_mouse(self, mouse: Mouse) -> bool:
        """Read the value of the input."""
        return mouse.button_state.get(self.key, False)


# TODO: MouseMoveControl and MouseScrollControl  # noqa: TD003
