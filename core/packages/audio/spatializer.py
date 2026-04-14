"""Audio spatializer computes spatial audio."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.packages.geometry.vector2 import Vector2


class AudioSpatializer2D:
    """Audio spatializer computes spatial audio 2D panning."""

    def __init__(self, min_distance: int, max_distance: int) -> None:
        """Initialize the spatializer with a min and max attenuation range."""
        self.min_distance = min_distance
        self.max_distance = max_distance

    def calculate(self, source: Vector2, listener: Vector2) -> tuple[float, float]:
        """Calculate the left right pan for 2D spatial audio between a listener and source."""
        dx = source.x - listener.x
        distance = source.distance_to(listener)

        # distance attenuation
        if distance <= self.min_distance:
            attenuation = 1.0
        elif distance >= self.max_distance:
            attenuation = 0.0
        else:
            t = (distance - self.min_distance) / (self.max_distance - self.min_distance)
            attenuation = 1.0 - t * t

        # avoid division by 0
        safe_max = max(self.max_distance, 0.0001)

        pan = max(-1.0, min(1.0, dx / safe_max))
        left = attenuation * (1 - max(0, pan))
        right = attenuation * (1 + min(0, pan))
        return left, right
