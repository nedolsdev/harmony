"""Wait for a given number of frames."""

from core.packages.timing.yield_instruction import YieldInstruction


class WaitForFrames(YieldInstruction):
    """Wait for a given number of frames."""

    def __init__(self, frames: int) -> None:
        """Initialize the WaitForFrames instruction with a number of frames."""
        if frames <= 0:
            msg = "WaitForFrames requires a positive integer number of frames."
            raise ValueError(msg)
        self.frames_remaining = frames

    def update(self) -> bool:
        """Update the instruction."""
        self.frames_remaining -= 1
        return self.frames_remaining <= 0


class WaitOneFrame(WaitForFrames):
    """Wait for one frame."""

    def __init__(self) -> None:
        """Initialize the WaitOneFrame instruction."""
        super().__init__(frames=1)
