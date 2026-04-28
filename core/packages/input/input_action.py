"""An action that is updated by an input."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from core.packages.input.action_phase import ActionPhase
from core.packages.input.input_value import InputValue

if TYPE_CHECKING:
    from collections.abc import Callable


class InputAction[InputValueT: InputValue]:
    """An action that is updated by an input."""

    def __init__(self, name: str, default_value: InputValueT) -> None:
        """Initialize the InputAction."""
        self.name = name
        self.phase: ActionPhase = ActionPhase.WAITING
        self.start_time: float | None = None

        # callbacks
        self._on_started: list[Callable[[InputAction[InputValueT]], None]] = []
        self._on_performed: list[Callable[[InputAction[InputValueT]], None]] = []
        self._on_cancelled: list[Callable[[InputAction[InputValueT]], None]] = []

        self.value = default_value

    def start(self) -> None:
        """Start the input action."""
        self.phase = ActionPhase.STARTED
        self.start_time = time.monotonic()

        for callback in self._on_started:
            callback(self)

    def perform(self) -> None:
        """Make the input action as performed."""
        self.phase = ActionPhase.PERFORMED

        for callback in self._on_performed:
            callback(self)

    def cancel(self) -> None:
        """Cancel the input action."""
        self.phase = ActionPhase.CANCELLED
        self.start_time = None

        for callback in self._on_cancelled:
            callback(self)

    def reset(self) -> None:
        """Set the interaction as waiting."""
        if self.phase in (ActionPhase.STARTED, ActionPhase.CANCELLED):
            self.phase = ActionPhase.WAITING
            self.start_time = None

    def has_started(self) -> bool:
        """Check if the InputAction has started."""
        return self.start_time is not None

    # callbacks register functions
    def on_started(self, callback: Callable[[InputAction[InputValueT]], None]) -> None:
        """Add callback for when InputAction is started."""
        self._on_started.append(callback)

    def on_performed(self, callback: Callable[[InputAction[InputValueT]], None]) -> None:
        """Add callback for when InputAction is performed."""
        self._on_performed.append(callback)

    def on_cancelled(self, callback: Callable[[InputAction[InputValueT]], None]) -> None:
        """Add callback for when InputAction is cancelled."""
        self._on_cancelled.append(callback)

    def get_value(self) -> InputValueT:
        """Get the current value of the action."""
        return self.value

    def as_composite_part[InputValueU: InputValue](self) -> InputValueU:
        """Return the action as a reference to a composite part."""
        return self  # ty:ignore[invalid-return-type]
