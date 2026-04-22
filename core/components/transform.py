"""Defines local and world spatial relationships."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.components.transform_base import TransformBase
from core.packages.animation.animatable import Animatable
from game.behavior import Behavior
from game.component_field import ComponentField, ComponentFields
from game.dirty import Dirtyable

if TYPE_CHECKING:
    from core.packages.animation.frame import ScalarFrame, Vector2Frame
    from core.packages.geometry.vector2 import Vector2


class Transform(Behavior, Animatable["TransformFields"], TransformBase):
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

    # animation

    @override
    @staticmethod
    def get_fields() -> type[TransformFields]:
        return TransformFields

    def animation_position(self, frame: Vector2Frame) -> None:
        """Animation position."""
        self.local_position = frame.vector

    def animate_scale(self, frame: Vector2Frame) -> None:
        """Animation scale."""
        self.local_scale = frame.vector

    def animate_rotation(self, frame: ScalarFrame) -> None:
        """Animation rotation."""
        self.local_rotation = frame.value


class TransformFields(ComponentFields):
    """The animatable component fields for the Transform component."""

    local_position: ComponentField[Vector2Frame, Transform] = ComponentField(
        lambda transform, frame: transform.animation_position(frame),
        component_type=Transform,
    )
    local_scale: ComponentField[Vector2Frame, Transform] = ComponentField(
        lambda transform, frame: transform.animate_scale(frame),
        component_type=Transform,
    )
    local_rotation: ComponentField[ScalarFrame, Transform] = ComponentField(
        lambda transform, frame: transform.animate_rotation(frame),
        component_type=Transform,
    )
