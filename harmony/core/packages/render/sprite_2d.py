"""The 2D sprite component."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

import pygame

from harmony.core.assets.sprite_image import SpriteImage
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.render import Render

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.camera.camera_component import Camera
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


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
    def fixed_update(self) -> None:
        """Update the sprite component in the physics / fixed loop."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the sprite at the given position."""
        local_size = Vector2(self.width, self.height)

        screen_size = camera.transform.inverse_transform_scale(transform.transform_scale(local_size))

        if self._dirty:
            # sprite is dirty, re-render

            if self.image:
                img = pygame.transform.scale(self.image.get_surface(), screen_size.as_tuple()).copy()
            else:
                img = SpriteImage.get_default_sprite_surface(screen_size.as_tuple())

            self.material.apply(img)

            # save the rendered surface for future use
            self._cached_surface = img.copy()

        else:
            # sprite is not dirty, use cached surface
            img = self._cached_surface
            if img is None:
                msg = "Sprite2D.render called as not 'dirty' without a cached surface."
                raise RuntimeError(msg)

        img = pygame.transform.rotate(img, math.degrees(transform.world_rotation))

        world_coords = transform.world_position
        screen_coords = camera.world_to_screen(world_coords)

        rect = img.get_rect(center=screen_coords.as_tuple())
        surface.blit(img, rect)

    def copy(self) -> Sprite2D:
        """Create a copy of the sprite component."""
        return Sprite2D(self.width, self.height, self.material, self.image)

    def mark_dirty(self) -> None:
        """Mark the sprite as dirty, indicating it needs to be redrawn."""
        self._dirty = True

    def is_dirty(self) -> bool:
        """Check if the sprite is marked as dirty."""
        return self._dirty

    def clear_dirty(self) -> None:
        """Clear the dirty flag for the sprite."""
        self._dirty = False
