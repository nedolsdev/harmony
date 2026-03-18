"""A special type of Transform that represents the rectangle that a UIElement can be placed inside of."""

from core.packages.geometry.vector2 import Vector2


class RectTransform:
    """A special type of Transform that represents the rectangle that a UIElement can be placed inside of."""

    def __init__(  # noqa: PLR0913
        self,
        position: Vector2,
        min_anchor: Vector2,
        max_anchor: Vector2,
        pivot: Vector2 | None = None,
        rotation: float | None = None,
        scale: Vector2 | None = None,
    ) -> None:
        """Initialize the RectTransform with a position."""
        # rect stuff
        self.min_anchor = min_anchor
        self.max_anchor = max_anchor
        self.pivot = pivot or Vector2(0.5, 0.5)

        # transform stuff
        self._local_position = position
        self._local_rotation = rotation or 0
        self._local_scale = scale or Vector2.zero()
