"""A surface asset can return a pygame Surface to render."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.packages.geometry.vector2 import Vector2
from game.asset import Asset

if TYPE_CHECKING:
    import pygame


class SurfaceAsset(Asset, ABC):
    """A surface asset can return a pygame Surface to render."""

    def __init__(self) -> None:
        """Initialize the SurfaceAsset."""
        super().__init__()

    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        """Get the surface to render."""


class ScalableSurfaceAsset(SurfaceAsset, ABC):
    """A surface asset can return a pygame Surface to render for a given scale."""

    def get_surface(self) -> pygame.Surface:
        """Get the surface to render for a given size."""
        return self.get_surface_of_scale(Vector2(1, 1))

    @abstractmethod
    def get_surface_of_scale(self, scale: Vector2) -> pygame.Surface:
        """Get the surface to render for a given scale."""
