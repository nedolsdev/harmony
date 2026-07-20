"""A collision between two colliders."""

from __future__ import annotations

# things it could have:
# colliders, contact points, impulse, relative velocity, body
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.core.packages.collision.collider import Collider
    from harmony.core.packages.collision.contact import Contact


class Collision:
    """A collision between two colliders."""

    def __init__(self, collider_a: Collider, collider_b: Collider, contact: Contact | None) -> None:
        """Initialize the Collision."""
        self.collider_a = collider_a
        self.collider_b = collider_b
        self.contact = contact

    def get_inverse(self) -> Collision:
        """Get the inverse of the Collision."""
        return Collision(self.collider_b, self.collider_a, self.contact)
