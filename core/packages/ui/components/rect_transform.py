"""A special type of Transform that represents the rectangle that a UIElement can be placed inside of."""

from core.components.transform_base import TransformBase
from core.packages.geometry.vector2 import Vector2


class RectTransform(TransformBase):
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
