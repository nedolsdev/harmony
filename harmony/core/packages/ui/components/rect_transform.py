"""A special type of Transform that represents the rectangle that a UIElement can be placed inside of."""

from __future__ import annotations

from abc import ABC, abstractmethod

from harmony.core.components.transform_base import TransformBase
from harmony.core.packages.geometry.vector2 import Vector2


class RectTransform(TransformBase, ABC):
    """A special type of Transform that represents the rectangle that a UIElement can be placed inside of."""

    def __init__(  # noqa: PLR0913
        self,
        min_anchor: Vector2,
        max_anchor: Vector2,
        pivot: Vector2 | None = None,
        position: Vector2 | None = None,
        rotation: float | None = None,
        scale: Vector2 | None = None,
    ) -> None:
        """Initialize the RectTransform with a position."""
        super().__init__(local_position=position, local_rotation=rotation, local_scale=scale)

        # rect stuff
        self.min_anchor = min_anchor
        self.max_anchor = max_anchor
        self.pivot = pivot or Vector2(0.5, 0.5)

    def mark_dirty(self) -> None:
        """Mark the transform as dirty, needs to recompute the world position."""
        self._dirty = True

    @abstractmethod
    def get_parent_transform(self) -> RectTransform | None:
        """Get the parent transform from a given transform (that may not exist)."""
