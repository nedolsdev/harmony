"""Collision contact data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


@dataclass
class Contact:
    """Collision contact data between two RigidBody2D."""

    normal: Vector2
    penetration: float
    contact_points: list[Vector2]

    restitution: float

    static_friction: float
    dynamic_friction: float
