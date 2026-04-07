"""A base for basic transform operations independent of the Transform component."""

from __future__ import annotations

import math
from typing import Self

from core.packages.geometry.vector2 import Vector2


class TransformBase:
    """A base for basic transform operations independent of the Transform component."""

    def __init__(
        self,
        *args,  # noqa: ANN002
        local_position: Vector2 | None = None,
        local_scale: Vector2 | None = None,
        local_rotation: float | None = None,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """Initialize the Transform."""
        super().__init__(*args, **kwargs)

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
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_parent_transform(self) -> Self | None:
        """Get the parent transform from a given transform (that may not exist)."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def _recalculate_if_needed(self) -> None:
        if not self._dirty:
            return

        parent_t = self.get_parent_transform()

        if parent_t is None:
            # no parent so world is same as local
            self._world_position = self.local_position.copy()
            self._world_rotation = self.local_rotation
            self._world_scale = self.local_scale.copy()

        else:
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
        parent_t = self.get_parent_transform()

        if parent_t is None:
            self.local_position = world_pos.copy()
        else:
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

    def transform_scale(self, local: Vector2) -> Vector2:
        """Convert a local scale to world scale."""
        self._recalculate_if_needed()
        return local * self._world_scale

    def inverse_transform_scale(self, local: Vector2) -> Vector2:
        """Convert a world scale to local scale."""
        self._recalculate_if_needed()
        return Vector2(
            local.x / self.world_scale.x,
            local.y / self.world_scale.y,
        )
