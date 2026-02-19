"""A surface asset can return a pygame Surface to render."""

from abc import abstractmethod

import pygame

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
