"""Something that can be dirtied (usually by Transform)."""
from __future__ import annotations


class Dirtyable:
    """Something that can be dirtied (usually by Transform)."""

    def __init__(self) -> None:
        """Initialize as Dirty."""
        self._dirty = True

    def mark_dirty(self) -> None:
        """Mark as dirty."""
        self._dirty = True
