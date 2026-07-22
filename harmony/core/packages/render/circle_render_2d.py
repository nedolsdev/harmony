"""The 2D circle render component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.transform import transform_circle
from harmony.core.packages.render.primitive import CircleRenderPrimitive, RenderPrimitive, Stroke
from harmony.core.packages.render.render import Render
from harmony.game.material import NoMaterial

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.geometry.circle import Circle
    from harmony.core.packages.render.color import Color
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


class CircleRender2D(Render):
    """The 2D circle render component."""

    def __init__(
        self,
        circle: Circle,
        fill: Color,
        stroke: Stroke | None = None,
        material: Material | None = None,
    ) -> None:
        """Initialize a rect and material."""
        super().__init__()
        self.circle = circle
        self.fill = fill
        self.stroke = stroke or Stroke()
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
    def fixed_update(self) -> None:
        """Update the component in the physics / fixed loop."""

    @override
    def late_update(self) -> None:
        """Late update the component every frame."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
        return [
            CircleRenderPrimitive(transform_circle(self.circle, transform), self.fill, self.stroke, self.material),
        ]

    def copy(self) -> CircleRender2D:
        """Create a copy of the sprite component."""
        return CircleRender2D(self.circle.copy(), self.fill, self.stroke, self.material)
