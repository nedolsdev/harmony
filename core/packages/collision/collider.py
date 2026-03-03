"""The underlying collider that computes collisions between two like colliders."""

from typing import Self


class Collider:
    """The underlying collider that computes collisions between two like colliders."""

    def collides_with(self, other: Self) -> bool:
        """Check whether the Collider is colliding with another of the same type."""
        msg = f"'{self.__class__.__name__}' does not implement 'copy' method."
        raise NotImplementedError(msg)
