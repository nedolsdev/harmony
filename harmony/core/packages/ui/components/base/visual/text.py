"""Basic Text component for the UI package."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.rectangle import Rectangle
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.primitive import TextRenderPrimitive
from harmony.core.packages.ui.components.visual_element import VisualUIElement

if TYPE_CHECKING:
    from pygame.font import Font

    from harmony.core.components.transform import Transform
    from harmony.core.packages.render.color import Color
    from harmony.core.packages.render.primitive import RenderPrimitive
    from harmony.game.event_handler import EventHandler


class Text(VisualUIElement):
    """Basic Text component for the UI package."""

    def __init__(self, content: str, font: Font, color: Color, *, antialiased: bool = False) -> None:
        """Initialize the basic Text UI component."""
        super().__init__()
        self.content = content
        self.font = font
        self.color = color
        self.antialiased = antialiased

        # TODO: Compute rough rect bounding box of the text  # noqa: TD003
        self.rect = Rectangle(0, 0, Vector2(0, 0))

    @override
    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object."""
        return [
            TextRenderPrimitive(
                self.content,
                self.font,
                self.color,
                self.rect,
                None,
                antialiased=self.antialiased,
            ).transform(transform),
        ]

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
