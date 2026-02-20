"""2D line component."""

from typing import override

import pygame

from core.components.position import Position
from core.components.render import Render
from core.components.rotation import Rotation
from game.event_handler import EventHandler
from game.material import Material
from game.vector2 import Vector2


class Line2D(Render):
    """A 2D line component."""

    def __init__(
        self,
        start: Vector2,
        end: Vector2,
        width: int,
        material: Material,
    ) -> None:
        """Initialize the 2D line with a given start and end point."""
        super().__init__()
        self.start_pos = start
        self.end_pos = end
        self.width = width
        self.material = material

    @override
    def render(self, position: Position, surface: pygame.Surface, *, rotation: Rotation | None = None) -> None:
        """Render the sprite at the given position."""
        start_pixel = position.get_vector() - self.start_pos
        end_pixel = position.get_vector() - self.end_pos

        line_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.line(
            line_surface,
            (255, 255, 255, 255),
            start_pixel.as_int_tuple(),
            end_pixel.as_int_tuple(),
            self.width,
        )
        self.material.apply(line_surface)
        surface.blit(line_surface, (0, 0))

    def get_start_end(self) -> tuple[Vector2, Vector2]:
        """Return the start and end positions of the line."""
        return self.start_pos, self.end_pos

    def set_start_end(self, start: Vector2, end: Vector2) -> None:
        """Set the start and end positions of the line."""
        self.start_pos = start
        self.end_pos = end

    @override
    def awake(self) -> None:
        """Event call when the component instance is created."""

    @override
    def start(self) -> None:
        """Initialize the component."""

    @override
    def update(self) -> None:
        """Update the component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def copy(self) -> "Line2D":
        """Create a copy of the Line2D component."""
        return Line2D(
            start=self.start_pos,
            end=self.end_pos,
            width=self.width,
            material=self.material,
        )
