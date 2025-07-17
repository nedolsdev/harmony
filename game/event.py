"""The event module defines events and event listeners for the game."""

from collections.abc import Callable

import pygame

from world.state import GameState


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


class PygameKeydownEvent(PygameEvent):
    """A Pygame-specific event class for keydown events."""

    def __init__(self, event: pygame.event.Event) -> None:
        """Initialize the keydown event with the Pygame event object."""
        super().__init__(event)

        key: int = event.key
        self.key = key

        self.event_type = PygameKeydownEvent.get_name_from_key(key)

    @staticmethod
    def get_name_from_key(key: int) -> str:
        """Get the name of the event from its Pygame type and key."""
        event_name = PygameEvent.get_name_from_type(pygame.KEYDOWN)
        key_name = pygame.key.name(key)
        return f"{event_name} {key_name}"


class EventListener:
    """A simple event listener that can be used to listen for specific events."""

    def __init__(self, event_type: str, callback: Callable[[Event, GameState], None]) -> None:
        """Initialize the event listener with an event type and callback."""
        self.event_type = event_type
        self.callback = callback

    def handle_event(self, event: Event, state: GameState) -> None:
        """Handle the event by calling the callback."""
        self.callback(event, state)
