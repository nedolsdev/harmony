"""Defines local and world spatial relationships."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.components.transform_base import TransformBase
from core.packages.animation.animatable import Animatable
from core.packages.animation.frame import VectorFrame
from game.behavior import Behavior
from game.dirty import Dirtyable

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class Transform(Behavior, Animatable[VectorFrame], TransformBase):
    """Defines local and world spatial relationships."""

    def __init__(
        self,
        local_position: Vector2 | None = None,
        local_scale: Vector2 | None = None,
        local_rotation: float | None = None,
    ) -> None:
        """Initialize the Transform."""
        super().__init__(
            disallow_multiple_of_type=True,
            local_position=local_position,
            local_scale=local_scale,
            local_rotation=local_rotation,
        )

    @override
    def mark_dirty(self) -> None:
        """Mark the transform as dirty, needs to recompute the world position."""
        if self._dirty:
            return

        self._dirty = True

        dirtyables = self.game_object.get_components_of_any_type(Dirtyable)
        for dirtyable in dirtyables:
            dirtyable.mark_dirty()

        for child in self.game_object.children:
            child.get_component(Transform).mark_dirty()

    @override
    def get_parent_transform(self) -> TransformBase | None:
        """Get the parent transform from a given transform (that may not exist)."""
        parent = self.game_object.parent
        if parent is None:
            return None
        return parent.get_component(Transform)

    @override
    def copy(self) -> Transform:
        """Create a copy of the Transform component."""
        transform = Transform(self._local_position, self._local_scale, self._local_rotation)
        transform._world_position = self._world_position
        transform._world_rotation = self._world_rotation
        transform._world_scale = self._world_scale
        transform._dirty = self._dirty
        return transform

    # TODO: Use fields or similar to allow control for animating scale, position, rotation separately  # noqa: TD003
    @override
    def set_animation_frame(self, frame: VectorFrame) -> None:
        """Set the animation frame."""
        self.local_position = frame.vector
