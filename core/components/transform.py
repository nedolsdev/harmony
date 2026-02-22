"""Defines local and world spatial relationships."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

from core.packages.animation.animatable import Animatable
from core.packages.animation.frame import VectorFrame
from game.behavior import Behavior
from game.vector2 import Vector2

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class Transform(Behavior, Animatable[VectorFrame]):
    """Defines local and world spatial relationships."""

    def __init__(
        self,
        local_position: Vector2 | None = None,
        local_scale: Vector2 | None = None,
        local_rotation: float | None = None,
    ) -> None:
        """Initialize the Transform."""
        super().__init__(disallow_multiple_of_type=True)

        # use internal variables so setters trigger mark_dirty
        self._local_position: Vector2 = local_position or Vector2.zero()
        self._local_scale: Vector2 = local_scale or Vector2.one()

        # uses radians
        self._local_rotation: float = local_rotation or 0

        # cached world data (starts dirty so these will always be calculated)
        self._world_position: Vector2 = None  # pyright: ignore[reportAttributeAccessIssue]
        self._world_rotation: float = None  # pyright: ignore[reportAttributeAccessIssue]
        self._world_scale: Vector2 = None  # pyright: ignore[reportAttributeAccessIssue]

        self._dirty = True

    @property
    def local_position(self) -> Vector2:
        """Get local position."""
        return self._local_position

    @local_position.setter
    def local_position(self, value: Vector2) -> None:
        """Set local position and mark dirty."""
        self._local_position = value
        self.mark_dirty()

    @property
    def local_rotation(self) -> float:
        """Get local rotation in radians."""
        return self._local_rotation

    @local_rotation.setter
    def local_rotation(self, value: float) -> None:
        """Set local rotation and mark dirty."""
        self._local_rotation = value
        self.mark_dirty()

    @property
    def local_scale(self) -> Vector2:
        """Get local scale."""
        return self._local_scale

    @local_scale.setter
    def local_scale(self, value: Vector2) -> None:
        """Set local scale and mark dirty."""
        self._local_scale = value
        self.mark_dirty()

    def mark_dirty(self) -> None:
        """Mark the transform as dirty, needs to recompute the world position."""
        if self._dirty:
            return

        self._dirty = True

        for child in self.game_object.children:
            child.get_component(Transform).mark_dirty()

    def _recalculate_if_needed(self) -> None:
        if not self._dirty:
            return

        parent = self.game_object.parent

        if parent is None:
            # no parent so world is same as local
            self._world_position = self.local_position.copy()
            self._world_rotation = self.local_rotation
            self._world_scale = self.local_scale.copy()

        else:
            parent_t = parent.get_component(Transform)
            parent_t._recalculate_if_needed()  # noqa: SLF001

            self._world_scale = parent_t._world_scale * self.local_scale  # noqa: SLF001
            self._world_rotation = parent_t._world_rotation + self.local_rotation  # noqa: SLF001

            scaled = self.local_position * parent_t._world_scale  # noqa: SLF001

            cos_r = math.cos(parent_t._world_rotation)  # noqa: SLF001
            sin_r = math.sin(parent_t._world_rotation)  # noqa: SLF001

            rotated = Vector2(
                scaled.x * cos_r - scaled.y * sin_r,
                scaled.x * sin_r + scaled.y * cos_r,
            )

            self._world_position = parent_t._world_position + rotated  # noqa: SLF001

        self._dirty = False

    @property
    def world_position(self) -> Vector2:
        """Get world position."""
        self._recalculate_if_needed()
        return self._world_position

    @property
    def world_rotation(self) -> float:
        """Get world rotation in radians."""
        self._recalculate_if_needed()
        return self._world_rotation

    @property
    def world_scale(self) -> Vector2:
        """Get world scale."""
        self._recalculate_if_needed()
        return self._world_scale

    @world_position.setter
    def world_position(self, world_pos: Vector2) -> None:
        """Set the world position of the object."""
        parent = self.game_object.parent

        if parent is None:
            self.local_position = world_pos.copy()
        else:
            parent_t = parent.get_component(Transform)
            parent_t._recalculate_if_needed()  # noqa: SLF001

            delta = world_pos - parent_t._world_position  # noqa: SLF001

            cos_r = math.cos(-parent_t._world_rotation)  # noqa: SLF001
            sin_r = math.sin(-parent_t._world_rotation)  # noqa: SLF001

            unrotated = Vector2(
                delta.x * cos_r - delta.y * sin_r,
                delta.x * sin_r + delta.y * cos_r,
            )

            self.local_position = Vector2(
                unrotated.x / parent_t._world_scale.x,  # noqa: SLF001
                unrotated.y / parent_t._world_scale.y,  # noqa: SLF001
            )

        self.mark_dirty()

    def copy(self) -> Transform:
        """Create a copy of the Transform component."""
        transform = Transform(self._local_position, self._local_scale, self._local_rotation)
        transform._world_position = self._world_position
        transform._world_rotation = self._world_rotation
        transform._world_scale = self._world_scale
        transform._dirty = self._dirty
        return transform

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    # TODO: Use fields or similar to allow control for animating scale, position, rotation separately  # noqa: TD003
    def set_animation_frame(self, frame: VectorFrame) -> None:
        """Set the animation frame."""
        self.local_position = frame.vector

    def transform_point(self, local: Vector2) -> Vector2:
        """Convert a local-space point to world-space."""
        self._recalculate_if_needed()

        scaled = local * self._world_scale

        cos_r = math.cos(self._world_rotation)
        sin_r = math.sin(self._world_rotation)

        rotated = Vector2(
            scaled.x * cos_r - scaled.y * sin_r,
            scaled.x * sin_r + scaled.y * cos_r,
        )

        return self._world_position + rotated

    def inverse_transform_point(self, world: Vector2) -> Vector2:
        """Convert a world-space point to local-space."""
        self._recalculate_if_needed()

        delta = world - self._world_position

        cos_r = math.cos(-self._world_rotation)
        sin_r = math.sin(-self._world_rotation)

        unrotated = Vector2(
            delta.x * cos_r - delta.y * sin_r,
            delta.x * sin_r + delta.y * cos_r,
        )

        return Vector2(
            unrotated.x / self._world_scale.x,
            unrotated.y / self._world_scale.y,
        )

    def transform_direction(self, local: Vector2) -> Vector2:
        """Convert a local direction to world direction (no translation)."""
        self._recalculate_if_needed()

        scaled = local * self._world_scale

        cos_r = math.cos(self._world_rotation)
        sin_r = math.sin(self._world_rotation)

        return Vector2(
            scaled.x * cos_r - scaled.y * sin_r,
            scaled.x * sin_r + scaled.y * cos_r,
        )
