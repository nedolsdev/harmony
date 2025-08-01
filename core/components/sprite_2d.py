"""The 2D sprite component for the Agent World game."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.components.render import Render
from game.image_cache import ImageCache

if TYPE_CHECKING:
    from core.components.position import Position
    from game.event_handler import EventHandler
    from game.material import Material


class SpriteImage:
    """A class to represent a sprite image."""

    def __init__(self, image_path: str) -> None:
        """Initialize the sprite image with a file path."""
        self.image_path = image_path

    def load(self) -> pygame.Surface:
        """Lazily load and return the image surface."""
        return ImageCache.load(self.image_path)


class Sprite2D(Render):
    """A 2D sprite component for the Agent World game."""

    def __init__(self, width: int, height: int, material: Material, image: SpriteImage | None = None) -> None:
        """Initialize the 2D sprite with given width and height."""
        super().__init__()
        self.width = width
        self.height = height
        self.image = image
        self.material = material

    def get_dimensions(self) -> tuple[int, int]:
        """Return the width and height of the sprite."""
        return self.width, self.height

    def set_dimensions(self, width: int, height: int) -> None:
        """Set the width and height of the sprite."""
        self.width = width
        self.height = height

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, position: Position, surface: pygame.Surface) -> None:
        """Render the sprite at the given position."""
        if self.image:
            img = pygame.transform.scale(self.image.load(), (self.width, self.height)).copy()
        else:
            img = self.get_default_sprite_surface((self.width, self.height))

        self.material.apply(img)
        surface.blit(img, (position.x, position.y))

    def copy(self) -> Sprite2D:
        """Create a copy of the sprite component."""
        return Sprite2D(self.width, self.height, self.material, self.image)

    @staticmethod
    def get_default_sprite_surface(size: tuple[int, int]) -> pygame.Surface:
        """Return a default sprite surface with the given size."""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 255, 255, 255))
        return surface
