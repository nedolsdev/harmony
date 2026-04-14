"""Some MouseBindings that connects an InputAction to inputs on a mouse."""
from __future__ import annotations

from typing import TYPE_CHECKING

from core.packages.input.controls.mouse_control import MouseClickControl, MouseMoveControl, MouseScrollControl
from core.packages.input.input_binding import InputBinding
from core.packages.input.interactions.default import DefaultInteraction

if TYPE_CHECKING:
    from core.packages.input.input_action import InputAction
    from core.packages.input.interaction import Interaction
    from core.packages.input.processor import InputProcessor


class MouseClickBinding(InputBinding[float]):
    """A MouseClickBinding connects a button click to an input action."""

    def __init__(
        self,
        button_key: int,
        action: InputAction[float],
        interaction: Interaction[float],
        *,
        processors: list[InputProcessor[float]] | None = None,
    ) -> None:
        """Initialize the MouseClickBinding."""
        control = MouseClickControl(key=button_key)
        super().__init__(control, action, interaction, processors=processors)


class MouseMoveBinding(InputBinding[tuple[float, float]]):
    """A MouseMoveBinding connects a mouse movement to an input action."""

    def __init__(
        self,
        action: InputAction[tuple[float, float]],
        interaction: Interaction[tuple[float, float]] | None = None,
        *,
        processors: list[InputProcessor[tuple[float, float]]] | None = None,
    ) -> None:
        """Initialize the MouseMoveBinding."""
        control = MouseMoveControl()
        super().__init__(control, action, interaction or DefaultInteraction(), processors=processors)


class MouseScrollBinding(InputBinding[tuple[float, float]]):
    """A MouseScrollBinding connects a mouse scroll to an input action."""

    def __init__(
        self,
        action: InputAction[tuple[float, float]],
        interaction: Interaction[tuple[float, float]],
        *,
        processors: list[InputProcessor[tuple[float, float]]] | None = None,
    ) -> None:
        """Initialize the MouseMoveBinding."""
        control = MouseScrollControl()
        super().__init__(control, action, interaction, processors=processors)
