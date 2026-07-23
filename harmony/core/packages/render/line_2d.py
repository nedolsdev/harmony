"""2D line component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.transform import transform_line_segment
from harmony.core.packages.render.primitive import Line2DRenderPrimitive, RenderPrimitive
from harmony.core.packages.render.render import Render

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.geometry.line_segment import LineSegment
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


class Line2D(Render):
    """A 2D line component."""

    def __init__(
        self,
        line_segment: LineSegment,
        width: int,
        material: Material,
    ) -> None:
        """Initialize the 2D line with a given start and end point."""
        super().__init__()
        self.segment = line_segment
        self.width = width
        self.material = material

    @override
    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
        return [Line2DRenderPrimitive(transform_line_segment(self.segment, transform), self.width, self.material)]

    def get_segment(self) -> LineSegment:
        """Return the start and end positions of the line."""
        return self.segment

    def set_segment(self, segment: LineSegment) -> None:
        """Set the start and end positions of the line."""
        self.segment = segment

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

    def copy(self) -> Line2D:
        """Create a copy of the Line2D component."""
        return Line2D(
            line_segment=self.segment.copy(),
            width=self.width,
            material=self.material,
        )
