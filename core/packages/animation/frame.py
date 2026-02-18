"""An AnimationFrame is a single state in time of an AnimationClip in progress."""

from typing import Generic, TypeVar


class AnimationFrame:
    """An AnimationFrame is a single state in time of an AnimationClip in progress."""


T = TypeVar("T", bound=tuple)


class VectorFrame(AnimationFrame, Generic[T]):
    """Frame with a vector of some values T."""

    def __init__(self, vector: T, *, first: bool = False) -> None:
        """Frame with a vector of values T."""
        self.vector = vector
        self.first = first
