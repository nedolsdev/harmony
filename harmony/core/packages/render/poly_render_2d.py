"""The 2D polygon render component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.transform import transform_polygon
from harmony.core.packages.render.primitive import PolygonRenderPrimitive, RenderPrimitive, Stroke
from harmony.core.packages.render.render import Render
from harmony.game.material import NoMaterial

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.geometry.polygon import Polygon
    from harmony.core.packages.render.color import Color
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


class PolyRender2D(Render):
    """The 2D polygon render component."""

    def __init__(
        self,
        polygon: Polygon,
        fill: Color,
        stroke: Stroke | None = None,
        material: Material | None = None,
    ) -> None:
        """Initialize a polygon and material."""
        super().__init__()
        self.polygon = polygon
        self.fill = fill
        self.stroke = stroke or Stroke()
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

    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
        return [
            PolygonRenderPrimitive(transform_polygon(self.polygon, transform), self.fill, self.stroke, self.material),
        ]

    def copy(self) -> PolyRender2D:
        """Create a copy of the sprite component."""
        return PolyRender2D(self.polygon.copy(), self.fill, self.stroke, self.material)
