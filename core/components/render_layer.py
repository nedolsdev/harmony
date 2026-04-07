"""Render layer component to manage rendering order of objects."""
from __future__ import annotations

from typing import TYPE_CHECKING

from game.component import GameComponent

if TYPE_CHECKING:
    from game.event_handler import EventHandler
    from game.sorting_layer import SortingLayer


class RenderLayer(GameComponent):
    """A render layer component that assigns a sorting layer to a game object."""

    def __init__(self, layer: SortingLayer) -> None:
        """Initialize the render layer with a sorting layer and order within that layer."""
        super().__init__(disallow_multiple_of_type=True)
        self.sorting_layer = layer
        self.order_in_layer: int | None = None

    def set_rendering_layer(self, layer: SortingLayer) -> None:
        """Set the sorting layer of the render layer. Also resets order in layer to None."""
        self.sorting_layer = layer
        self.order_in_layer = None

    def set_order_in_layer(self, order: int) -> None:
        """Set the order within the sorting layer."""
        self.order_in_layer = order

    def awake(self) -> None:
        """Event call when the script instance is created."""

    def start(self) -> None:
        """Start the render layer component."""

    def update(self) -> None:
        """Update the render layer component."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def copy(self) -> RenderLayer:
        """Create a copy of the render layer component."""
        new_layer = RenderLayer(self.sorting_layer)
        new_layer.order_in_layer = self.order_in_layer
        return new_layer
