"""Basic Text component for the UI package."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.ui.components.visual_element import VisualUIElement

if TYPE_CHECKING:
    from pygame.font import Font

    from harmony.core.components.transform import Transform
    from harmony.core.packages.render.color import Color
    from harmony.core.packages.render.primitive import RenderPrimitive
    from harmony.game.event_handler import EventHandler


class Text(VisualUIElement):
    """Basic Text component for the UI package."""

    def __init__(self, content: str, font: Font, color: Color) -> None:
        """Initialize the basic Text UI component."""
        super().__init__()
        self.content = content
        self.font = font
        self.color = color

    @override
    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object."""
        # TODO: Render text  # noqa: TD003
        return []

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
