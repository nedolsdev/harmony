"""An AnimationFrame is a single state in time of an AnimationClip in progress."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class AnimationFrame:
    """An AnimationFrame is a single state in time of an AnimationClip in progress."""


class VectorFrame(AnimationFrame):
    """Frame with a Vector2."""

    def __init__(self, vector: Vector2) -> None:
        """Frame with a Vector2."""
        self.vector = vector
