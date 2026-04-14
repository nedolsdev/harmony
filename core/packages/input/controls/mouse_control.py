"""Some different mouse controls."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.input.controls.mouse_input import MouseInputControl

if TYPE_CHECKING:
    from core.packages.input.controls.devices.mouse import Mouse


class MouseClickControl(MouseInputControl[bool]):
    """A control defined as the click of a mouse."""

    def __init__(self, key: int) -> None:
        """Initialize the MouseClickControl."""
        super().__init__()
        self.key = key

    @override
    def read_value_from_mouse(self, mouse: Mouse) -> bool:
        """Read the value of the input."""
        return mouse.button_state.get(self.key, False)


class MouseMoveControl(MouseInputControl[tuple[float, float]]):
    """A control defined as a movement of a mouse."""

    @override
    def read_value_from_mouse(self, mouse: Mouse) -> tuple[float, float]:
        """Read the value of the input. Return as (dx, dy)."""
        return mouse.relative


class MouseScrollControl(MouseInputControl[tuple[float, float]]):
    """A control defined as scrolling a mouse."""

    @override
    def read_value_from_mouse(self, mouse: Mouse) -> tuple[float, float]:
        """Read the value of the input. Return as (dx, dy)."""
        return mouse.scroll
