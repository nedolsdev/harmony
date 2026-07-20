"""Collision test component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.game.behavior import Behavior

if TYPE_CHECKING:
    from harmony.core.packages.collision.collision import Collision


class CollisionTest(Behavior):
    """A component that uses a timer."""

    @override
    def copy(self) -> CollisionTest:
        """Create a copy of the timer component."""
        return self

    @override
    def on_collision_enter(self, collision: Collision) -> None:
        print("Collision enter!")  # noqa: T201

    @override
    def on_collision_stay(self, collision: Collision) -> None:
        print("Collision stay!")  # noqa: T201

    @override
    def on_collision_exit(self, collision: Collision) -> None:
        print("Collision exit!")  # noqa: T201
