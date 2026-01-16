"""The 2D sprite component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.components.render import Render
from game.image_cache import ImageCache

if TYPE_CHECKING:
    from core.components.position import Position
    from core.components.rotation import Rotation
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
    """A 2D sprite component."""

    def __init__(self, width: int, height: int, material: Material, image: SpriteImage | None = None) -> None:
        """Initialize the 2D sprite with given width and height."""
        super().__init__()
        self.width = width
        self.height = height
        self.image = image
        self.material = material

        # starts dirty to ensure it is rendered on first update
        self._dirty = True
        self._cached_surface: pygame.Surface | None = None

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

    def render(self, position: Position, surface: pygame.Surface, *, rotation: Rotation | None = None) -> None:
        """Render the sprite at the given position."""
        if self._dirty:
            # sprite is dirty, re-render

            if self.image:
                img = pygame.transform.scale(self.image.load(), (self.width, self.height)).copy()
            else:
                img = self.get_default_sprite_surface((self.width, self.height))

            self.material.apply(img)

            # save the rendered surface for future use
            self._cached_surface = img.copy()
            self._dirty = False

        else:
            # sprite is not dirty, use cached surface
            img = self._cached_surface
            if img is None:
                msg = "Sprite2D.render called as not 'dirty' without a cached surface."
                raise RuntimeError(msg)

        if rotation:
            img = pygame.transform.rotate(img, rotation.get_degrees())

        rect = img.get_rect(center=position.to_tuple())
        surface.blit(img, rect)

    def copy(self) -> Sprite2D:
        """Create a copy of the sprite component."""
        return Sprite2D(self.width, self.height, self.material, self.image)

    @staticmethod
    def get_default_sprite_surface(size: tuple[int, int]) -> pygame.Surface:
        """Return a default sprite surface with the given size."""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 255, 255, 255))
        return surface

    def mark_dirty(self) -> None:
        """Mark the sprite as dirty, indicating it needs to be redrawn."""
        self._dirty = True

    def is_dirty(self) -> bool:
        """Check if the sprite is marked as dirty."""
        return self._dirty

    def clear_dirty(self) -> None:
        """Clear the dirty flag for the sprite."""
        self._dirty = False
