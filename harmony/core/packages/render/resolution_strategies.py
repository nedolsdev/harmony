"""Some resolution strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from harmony.core.packages.geometry.vector2 import Vector2


@dataclass(frozen=True)
class ResolutionTransform:
    """Resolution transform data for a resolution strategy."""

    size: Vector2
    position: Vector2


class ResolutionStrategy(ABC):
    """A way to resolve the difference between world and screen resolutions."""

    @abstractmethod
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        """Compute the transform from logical to screen space."""
        raise NotImplementedError


class StretchResolutionStrategy(ResolutionStrategy):
    """Stretch to fill the entire screen."""

    @override
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        return ResolutionTransform(
            size=screen_size,
            position=Vector2(0, 0),
        )


class FitResolutionStrategy(ResolutionStrategy):
    """Maintain aspect ratio with letterboxing."""

    @override
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        scale = min(
            screen_size.x / world_size.x,
            screen_size.y / world_size.y,
        )

        size = Vector2(
            world_size.x * scale,
            world_size.y * scale,
        )

        position = Vector2(
            (screen_size.x - size.x) / 2,
            (screen_size.y - size.y) / 2,
        )

        return ResolutionTransform(
            size=size,
            position=position,
        )


class FillResolutionStrategy(ResolutionStrategy):
    """Maintain aspect ratio while filling the entire screen with cropping."""

    @override
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        scale = max(
            screen_size.x / world_size.x,
            screen_size.y / world_size.y,
        )

        size = Vector2(
            world_size.x * scale,
            world_size.y * scale,
        )

        position = Vector2(
            (screen_size.x - size.x) / 2,
            (screen_size.y - size.y) / 2,
        )

        return ResolutionTransform(
            size=size,
            position=position,
        )


class IntegerFitResolutionStrategy(ResolutionStrategy):
    """Maintain aspect ratio using integer scaling."""

    @override
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        scale = max(
            1,
            int(
                min(
                    screen_size.x / world_size.x,
                    screen_size.y / world_size.y,
                ),
            ),
        )

        size = Vector2(
            world_size.x * scale,
            world_size.y * scale,
        )

        position = Vector2(
            (screen_size.x - size.x) / 2,
            (screen_size.y - size.y) / 2,
        )

        return ResolutionTransform(
            size=size,
            position=position,
        )


class IntegerFillResolutionStrategy(ResolutionStrategy):
    """Fill the screen using integer scaling with cropping."""

    @override
    def compute_transform(
        self,
        world_size: Vector2,
        screen_size: Vector2,
    ) -> ResolutionTransform:
        scale = max(
            1,
            int(
                max(
                    screen_size.x / world_size.x,
                    screen_size.y / world_size.y,
                ),
            ),
        )

        size = Vector2(
            world_size.x * scale,
            world_size.y * scale,
        )

        position = Vector2(
            (screen_size.x - size.x) / 2,
            (screen_size.y - size.y) / 2,
        )

        return ResolutionTransform(
            size=size,
            position=position,
        )
