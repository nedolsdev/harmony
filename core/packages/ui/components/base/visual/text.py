"""Basic Text component for the UI package."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.ui.components.visual_element import VisualUIElement

if TYPE_CHECKING:
    import pygame
    from pygame.font import Font

    from core.components.transform import Transform
    from core.packages.camera.camera_component import Camera
    from game.event_handler import EventHandler


class Text(VisualUIElement):
    """Basic Text component for the UI package."""

    def __init__(self, content: str, font: Font, color: tuple[int, int, int]) -> None:
        """Initialize the basic Text UI component."""
        super().__init__()
        self.content = content
        self.font = font
        self.color = color

    @override
    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the object."""
        # TODO: Don't always assume screen space  # noqa: TD003
        screen_coords = transform.local_position
        surface.blit(self.font.render(self.content, antialias=True, color=self.color), screen_coords.as_tuple())

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

    def copy(self) -> Text:
        """Copy the component."""
        return Text(content=self.content, font=self.font, color=self.color)
