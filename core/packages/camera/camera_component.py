"""The Camera component."""

from __future__ import annotations

from typing import override

from core.components.transform import Transform
from core.packages.geometry.vector2 import Vector2
from game.behavior import Behavior
from game.error import MissingComponentDependencyError


class Viewport:
    """Viewport of a screen or screen subsection."""

    def __init__(self, width: int, height: int, offset: Vector2 | None = None) -> None:
        """Initialize the Viewport."""
        self.width = width
        self.height = height
        self.offset = offset or Vector2(0, 0)

    def as_tuple(self) -> tuple[int, int, int, int]:
        """As a (x, y, w, h) tuple."""
        return (int(self.offset.x), int(self.offset.y), self.width, self.height)


class Camera(Behavior):
    """The Camera component."""

    transform: Transform

    def __init__(self, viewport: Viewport) -> None:
        """Initialize the Camera component."""
        super().__init__()
        self.viewport = viewport

    def world_to_screen(self, world: Vector2) -> Vector2:
        """Convert a world-space point to screen-space."""
        return self.transform.inverse_transform_point(world)

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        if not self.game_object.has_component(Transform):
            msg = "Camera does not have necessary 'Transform' component attached."
            raise MissingComponentDependencyError(msg)

        self.transform = self.game_object.get_component(Transform)

    @override
    def copy(self) -> Camera:
        """Copy the camera component."""
        return Camera(Viewport(self.viewport.width, self.viewport.height, self.viewport.offset.copy()))
