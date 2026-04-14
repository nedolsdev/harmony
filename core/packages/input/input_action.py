"""An action that is updated by an input."""

import time

from core.packages.input.action_phase import ActionPhase


class InputAction:
    """An action that is updated by an input."""

    def __init__(self, name: str) -> None:
        """Initialize the InputAction."""
        self.name = name
        self.phase: ActionPhase = ActionPhase.WAITING
        self.start_time: float | None = None

    def start(self) -> None:
        """Start the input action."""
        self.phase = ActionPhase.STARTED
        self.start_time = time.time()

    def perform(self) -> None:
        """Make the input action as performed."""
        self.phase = ActionPhase.PERFORMED

    def cancel(self) -> None:
        """Cancel the input action."""
        self.phase = ActionPhase.CANCELLED
        self.start_time = None

    def reset(self) -> None:
        """Set the interaction as waiting."""
        if self.phase in (ActionPhase.STARTED, ActionPhase.CANCELLED):
            self.phase = ActionPhase.WAITING
            self.start_time = None

    def has_started(self) -> bool:
        """Check if the InputAction has started."""
        return self.start_time is not None
