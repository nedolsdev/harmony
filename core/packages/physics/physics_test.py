"""A component that tests some physics stuff."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.geometry.vector2 import Vector2
from core.packages.physics.rigidbody_2d import RigidBody2D
from core.packages.timing.coroutine_decorator import coroutine
from core.packages.timing.instructions.wait_for_seconds import WaitForSeconds
from game.behavior import Behavior

if TYPE_CHECKING:
    from core.packages.timing.coroutine import CoroutineGenerator


class PhysicsTest(Behavior):
    """A component that uses a timer."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""
        self.start_coroutine(self.apply_impulse())

    @override
    def copy(self) -> PhysicsTest:
        """Create a copy of the timer component."""
        return self

    @override
    def fixed_update(self) -> None:
        """Update the component in the physics / fixed loop."""

    @coroutine
    def apply_impulse(self) -> CoroutineGenerator:
        """Apply impulse after 1 second."""
        yield WaitForSeconds(1)
        self.game_object.get_component(RigidBody2D).apply_linear_impulse(Vector2(50, 50))
