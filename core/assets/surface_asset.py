"""A surface asset can return a pygame Surface to render."""

from abc import abstractmethod

import pygame

from core.packages.geometry.vector2 import Vector2
from game.asset import Asset


class SurfaceAsset(Asset):
    """A surface asset can return a pygame Surface to render."""

    def __init__(self) -> None:
        """Initialize the SurfaceAsset."""

    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        """Get the surface to render."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)


class ScalableSurfaceAsset(SurfaceAsset):
    """A surface asset can return a pygame Surface to render for a given scale."""

    def __init__(self) -> None:
        """Initialize the SurfaceAsset."""

    def get_surface(self) -> pygame.Surface:
        """Get the surface to render for a given size."""
        return self.get_surface_of_scale(Vector2(1, 1))

    @abstractmethod
    def get_surface_of_scale(self, scale: Vector2) -> pygame.Surface:
        """Get the surface to render for a given scale."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
