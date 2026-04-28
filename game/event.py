"""The event module defines events and event listeners for the game."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from collections.abc import Callable


class Event:
    """A simple event class to represent an event in the game."""

    def __init__(self, event_type: str) -> None:
        """Initialize the event with a type."""
        self.event_type = event_type


class PygameEvent(Event):
    """A Pygame-specific event class that extends the base Event class."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the Pygame event with the Pygame event object."""
        event_name = pygame.event.event_name(event.type)
        super().__init__(event_name)
        self.pygame_type = event.type

    @staticmethod
    def get_name_from_type(pygame_type: int) -> str:
        """Get the name of the event from its Pygame type."""
        return pygame.event.event_name(pygame_type)


class PygameKeyStateEvent(PygameEvent):
    """A Pygame-specific event class for key up/down events."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the keydown event with the Pygame event object."""
        super().__init__(event)

        self.key: int = event.key

        self.event_type = PygameKeyStateEvent.get_name_from_key(event.key, event.type)

    @staticmethod
    def get_name_from_key(key: int, event_type: int) -> str:
        """Get the name of the event from its Pygame type and key."""
        event_name = PygameEvent.get_name_from_type(event_type)
        key_name = pygame.key.name(key)
        return f"{event_name} {key_name}"


class PygameMouseStateEvent(PygameEvent):
    """A Pygame-specific event class for mouse button up/down events."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the mouse button event with the Pygame event object."""
        super().__init__(event)

        self.button: int = event.button

        self.event_type = PygameMouseStateEvent.get_name_from_button(self.button, event.type)

    @staticmethod
    def get_name_from_button(button: int, event_type: int) -> str:
        """Get the name of the event from its Pygame type and button."""
        event_name = PygameEvent.get_name_from_type(event_type)
        button_name = pygame.key.name(button)
        return f"{event_name} {button_name}"


class PygameMouseMoveEvent(PygameEvent):
    """A Pygame-specific event class for mouse move event."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the mouse move event with the Pygame event object."""
        super().__init__(event)

        self.pos: tuple[int, int] = event.pos
        self.rel: tuple[int, int] = event.rel


class PygameMouseWheelEvent(PygameEvent):
    """A Pygame-specific event class for mouse wheel scroll event."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the mouse wheel scroll event with the Pygame event object."""
        super().__init__(event)

        self.x: int = event.x
        self.y: int = event.y


class EventListener:
    """A simple event listener that can be used to listen for specific events."""

    def __init__(self, event_type: str, callback: Callable[[], None]) -> None:
        """Initialize the event listener with an event type and callback."""
        self.event_type = event_type
        self.callback = callback

    def handle_event(self) -> None:
        """Handle the event by calling the callback."""
        self.callback()
