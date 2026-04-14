"""An action that is updated by an input."""

from __future__ import annotations

import time
from collections.abc import Callable

from core.packages.input.action_phase import ActionPhase

type PhaseCallback = Callable[[InputAction], None]


class InputAction:
    """An action that is updated by an input."""

    # last value
    value: float

    def __init__(self, name: str) -> None:
        """Initialize the InputAction."""
        self.name = name
        self.phase: ActionPhase = ActionPhase.WAITING
        self.start_time: float | None = None

        # callbacks
        self._on_started: list[PhaseCallback] = []
        self._on_performed: list[PhaseCallback] = []
        self._on_cancelled: list[PhaseCallback] = []

    def start(self) -> None:
        """Start the input action."""
        self.phase = ActionPhase.STARTED
        self.start_time = time.time()

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
    def on_started(self, callback: PhaseCallback) -> None:
        """Add callback for when InputAction is started."""
        self._on_started.append(callback)

    def on_performed(self, callback: PhaseCallback) -> None:
        """Add callback for when InputAction is performed."""
        self._on_performed.append(callback)

    def on_cancelled(self, callback: PhaseCallback) -> None:
        """Add callback for when InputAction is cancelled."""
        self._on_cancelled.append(callback)
