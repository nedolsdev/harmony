"""Yield step in Coroutine."""


class YieldInstruction:
    """Yield step in Coroutine."""

    def update(self) -> bool:
        """Update the yield instruction. Returns True when completed."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
