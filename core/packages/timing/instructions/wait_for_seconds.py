"""Wait for seconds (scaled delta time) YieldInstruction."""
from __future__ import annotations

from core.packages.timing.delta_time import DeltaTime
from core.packages.timing.yield_instruction import YieldInstruction


class WaitForSeconds(YieldInstruction):
    """Wait for a given number of seconds (scaled)."""

    def __init__(self, seconds: float) -> None:
        """Initialize the WaitForSeconds instruction with a number of seconds."""
        self.time_remaining = seconds

    def update(self) -> bool:
        """Update the instruction."""
        self.time_remaining -= DeltaTime.get_delta_time()
        return self.time_remaining <= 0
