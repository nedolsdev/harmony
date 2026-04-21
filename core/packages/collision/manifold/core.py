"""A collision manifold."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


@dataclass
class Manifold:
    """A collision manifold."""

    normal: Vector2
    penetration: float
    contacts: list[Vector2]
