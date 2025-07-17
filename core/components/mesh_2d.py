"""The 2D mesh component for the Agent World game."""

from typing import override

import pygame

from core.components.position import Position
from core.components.render import Render
from game.event_handler import EventHandler


class Material:
    """A simple material class to hold color information."""

    def __init__(self, color: tuple[int, int, int]) -> None:
        """Initialize the material with a color."""
        self.color = color


class Mesh2D(Render):
    """A 2D mesh component for the Agent World game."""

    def __init__(self, width: int, height: int, material: Material) -> None:
        """Initialize the 2D mesh with given width and height."""
        super().__init__()
        self.width = width
        self.height = height
        self.material = material

    def get_dimensions(self) -> tuple[int, int]:
        """Return the width and height of the mesh."""
        return self.width, self.height

    def set_dimensions(self, width: int, height: int) -> None:
        """Set the width and height of the mesh."""
        self.width = width
        self.height = height

    @override
    def start(self) -> None:
        """Initialize the mesh component."""

    @override
    def update(self) -> None:
        """Update the mesh component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def render(self, position: Position, surface: pygame.Surface) -> None:
        """Render the mesh at the given position."""
        mesh = self
        rect = pygame.Rect(position.x, position.y, mesh.width, mesh.height)
        pygame.draw.rect(surface, mesh.material.color, rect)
