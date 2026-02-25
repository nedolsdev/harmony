"""The 2D polygon render component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.components.render import Render
from game.material import NoMaterial

if TYPE_CHECKING:
    import pygame

    from core.assets.polygon import Polygon
    from core.components.transform import Transform
    from core.packages.camera.camera_component import Camera
    from game.event_handler import EventHandler
    from game.material import Material


class PolyRender2D(Render):
    """The 2D polygon render component."""

    def __init__(self, polygon: Polygon, material: Material | None = None) -> None:
        """Initialize a polygon and material."""
        super().__init__()
        self.polygon = polygon
        self.material = material or NoMaterial()

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the polygon render component."""

    @override
    def update(self) -> None:
        """Update the polygon render component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the polygon at the given position."""
        poly_surface = self.polygon.get_surface()

        self.material.apply(poly_surface)

        world_coords = transform.world_position
        screen_coords = camera.world_to_screen(world_coords)

        surface.blit(poly_surface, screen_coords.as_tuple())

    def copy(self) -> PolyRender2D:
        """Create a copy of the sprite component."""
        return PolyRender2D(self.polygon.copy(), self.material)
