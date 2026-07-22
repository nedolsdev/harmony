"""The 2D rect render component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.transform import transform_rectangle
from harmony.core.packages.render.primitive import RectRenderPrimitive, RenderPrimitive, Stroke
from harmony.core.packages.render.render import Render
from harmony.game.material import NoMaterial

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.geometry.rectangle import Rectangle
    from harmony.core.packages.render.color import Color
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


class RectRender2D(Render):
    """The 2D rect render component."""

    def __init__(self, rect: Rectangle, fill: Color, stroke: Stroke, material: Material | None = None) -> None:
        """Initialize a rect and material."""
        super().__init__()
        self.rect = rect
        self.fill = fill
        self.stroke = stroke
        self.material = material or NoMaterial()

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the rect render component."""

    @override
    def update(self) -> None:
        """Update the rect render component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
        return [
            RectRenderPrimitive(transform_rectangle(self.rect, transform), self.fill, self.stroke, self.material),
        ]

    def copy(self) -> RectRender2D:
        """Create a copy of the sprite component."""
        return RectRender2D(self.rect.copy(), self.fill, self.stroke, self.material)
