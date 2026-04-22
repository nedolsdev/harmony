"""An AnimationFrame is a single state in time of an AnimationClip in progress."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class AnimationFrame:
    """An AnimationFrame is a single state in time of an AnimationClip in progress."""

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def __hash__(self) -> int:
        """Hash."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)


class Vector2Frame(AnimationFrame):
    """Frame with a Vector2."""

    def __init__(self, vector: Vector2) -> None:
        """Frame with a Vector2."""
        self.vector = vector

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Vector2Frame):
            return False
        return self.vector == other.vector

    def __hash__(self) -> int:
        """Hash."""
        return hash((self.vector.x, self.vector.y))


class ScalarFrame(AnimationFrame):
    """Frame with a single scalar value."""

    def __init__(self, value: float) -> None:
        """Frame with a single scalar value."""
        self.value = value

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, ScalarFrame):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash."""
        return hash(self.value)
