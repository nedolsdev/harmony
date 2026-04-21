"""CollisionSurface defines how the collision interacts (slippery, bouncy, etc.)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollisionSurface:
    """CollisionSurface defines how the collision interacts (slippery, bouncy, etc.)."""

    restitution: float = 0.2
    static_friction: float = 0.5
    dynamic_friction: float = 0.3


DEFAULT_SURFACE = CollisionSurface(0.2, 0.5, 0.3)
BOUNCY_SURFACE = CollisionSurface(0.2, 0.5, 0.3)
ICE_SURFACE = CollisionSurface(0.0, 0.05, 0.02)
RUBBER_SURFACE = CollisionSurface(0.6, 0.9, 0.8)
