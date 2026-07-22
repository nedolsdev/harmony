"""Resolution manager."""

from __future__ import annotations

import pygame

from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.resolution_strategies import IntegerFitResolutionStrategy, ResolutionStrategy


class ResolutionManager:
    """Resolution manager."""

    def __init__(
        self,
        resolution_strategy: ResolutionStrategy | None = None,
    ) -> None:
        """Initialize the ResolutionManager."""
        self._resolution: tuple[int, int] | None = None
        self.strategy = resolution_strategy or IntegerFitResolutionStrategy()

    def set_logical_resolution(
        self,
        resolution: tuple[int, int] | None,
    ) -> None:
        """Set the logical resolution."""
        self._resolution = resolution

    def get_logical_resolution(
        self,
    ) -> tuple[int, int] | None:
        """Get the logical resolution."""
        return self._resolution

    def set_strategy(
        self,
        strategy: ResolutionStrategy,
    ) -> None:
        """Set the resolution strategy."""
        self.strategy = strategy

    def apply(
        self,
        logical_surface: pygame.Surface,
        screen_surface: pygame.Surface,
        *,
        use_smooth_scaling: bool = False,
    ) -> None:
        """Apply the logical surface to the screen surface."""
        world_size = (
            Vector2(*self._resolution) if self._resolution is not None else Vector2(*logical_surface.get_size())
        )

        transform = self.strategy.compute_transform(
            world_size,
            Vector2(*screen_surface.get_size()),
        )

        scaled = self.scale_surface(
            logical_surface,
            transform.size,
            use_smooth_scaling=use_smooth_scaling,
        )

        screen_surface.blit(
            scaled,
            transform.position.as_tuple(),
        )

    @staticmethod
    def scale_surface(
        surface: pygame.Surface,
        size: Vector2,
        *,
        use_smooth_scaling: bool = False,
    ) -> pygame.Surface:
        """Scale a surface to the given size."""
        scaled_size = (
            max(1, round(size.x)),
            max(1, round(size.y)),
        )

        if scaled_size == surface.get_size():
            return surface.copy()

        if use_smooth_scaling:
            return pygame.transform.smoothscale(
                surface,
                scaled_size,
            )

        return pygame.transform.scale(
            surface,
            scaled_size,
        )
