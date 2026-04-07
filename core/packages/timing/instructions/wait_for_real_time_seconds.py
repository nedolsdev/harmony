"""Wait for real time seconds (unscaled delta time) YieldInstruction."""
from __future__ import annotations

from core.packages.timing.delta_time import DeltaTime
from core.packages.timing.yield_instruction import YieldInstruction


class WaitForRealTimeSeconds(YieldInstruction):
    """Wait for a given number of seconds (unscaled)."""

    def __init__(self, seconds: float) -> None:
        """Initialize the WaitForRealTimeSeconds instruction with a number of seconds."""
        self.time_remaining = seconds

    def update(self) -> bool:
        """Update the instruction."""
        self.time_remaining -= DeltaTime.get_unscaled_delta_time()
        return self.time_remaining <= 0
