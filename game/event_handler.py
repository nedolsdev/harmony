"""The event handler module manages input events for the game."""
from __future__ import annotations

from typing import TYPE_CHECKING

from game.event import Event, EventListener

if TYPE_CHECKING:
    from collections.abc import Callable


class EventHandler:
    """Handles input events for the game."""

    def __init__(self) -> None:
        """Initialize the event handler."""
        self.event_listeners: dict[str, list[EventListener]] = {}

    def handle_events(self, events: list[Event]) -> None:
        """Process input events and update the game state."""
        for event in events:
            self.handle_event(event)

    def handle_event(self, event: Event) -> None:
        """Handle a single event to update the game state."""
        if event.event_type in self.event_listeners:
            for listener in self.event_listeners[event.event_type]:
                listener.handle_event()

    def register_listener(self, event_type: str, callback: Callable[[], None]) -> None:
        """Register a new event listener."""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(EventListener(event_type, callback))

    def unregister_listener(self, event_type: str, callback: Callable[[], None]) -> None:
        """Unregister an existing event listener."""
        if event_type in self.event_listeners:
            self.event_listeners[event_type] = [
                listener for listener in self.event_listeners[event_type] if listener.callback != callback
            ]
            if not self.event_listeners[event_type]:
                del self.event_listeners[event_type]
        else:
            msg = f"No listeners registered for event type: {event_type}"
            raise LookupError(msg)
