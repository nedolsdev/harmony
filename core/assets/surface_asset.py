"""A surface asset can return a pygame Surface to render."""

from abc import abstractmethod

import pygame

from game.asset import Asset
from game.vector2 import Vector2


class SurfaceAsset(Asset):
    """A surface asset can return a pygame Surface to render."""

    def __init__(self) -> None:
        """Initialize the SurfaceAsset."""

    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        """Get the surface to render."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)


class ResizableSurfaceAsset(SurfaceAsset):
    """A surface asset can return a pygame Surface to render for a given size."""

    def __init__(self) -> None:
        """Initialize the SurfaceAsset."""

    def get_surface(self) -> pygame.Surface:
        """Get the surface to render for a given size."""
        return self.get_surface_of_size(Vector2(1, 1))

    @abstractmethod
    def get_surface_of_size(self, size: Vector2) -> pygame.Surface:
        """Get the surface to render for a given size."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
