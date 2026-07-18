"""Event backend sources events to be consumed by the event handler."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

import pygame

from harmony.game.event import (
    PygameEvent,
    PygameKeyStateEvent,
    PygameMouseMoveEvent,
    PygameMouseStateEvent,
    PygameMouseWheelEvent,
)

if TYPE_CHECKING:
    from harmony.game.event import Event


class EventBackend(ABC):
    """Event backend sources events to be consumed by the event handler."""

    def __init__(self) -> None:
        """Initialize the EventBackend."""
        self.event_buffer: list[Event] = []

    @abstractmethod
    def poll(self) -> None:
        """Add new events to the buffer."""

    def fetch(self) -> list[Event]:
        """Fetch events."""
        return self.event_buffer

    def clear(self) -> None:
        """Clear the event buffer."""
        self.event_buffer = []


class PygameEventBackend(EventBackend):
    """Pygame event backend."""

    @override
    def poll(self) -> None:
        """Add new events to the buffer."""
        pygame_events = pygame.event.get()

        for event in pygame_events:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.event_buffer.append(PygameKeyStateEvent(event))
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self.event_buffer.append(PygameMouseStateEvent(event))
            if event.type == pygame.MOUSEMOTION:
                self.event_buffer.append(PygameMouseMoveEvent(event))
            if event.type == pygame.MOUSEWHEEL:
                self.event_buffer.append(PygameMouseWheelEvent(event))
            else:
                self.event_buffer.append(PygameEvent(event))
