"""The component module defines the base class for game components."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from game.event_handler import EventHandler


class GameComponent:
    """A base class for game components that can be added to the game state."""

    def __init__(self) -> None:
        """Initialize the game component."""
        self.active = True

    @abstractmethod
    def awake(self) -> None:
        """Event call when the script instance is created."""
        msg = f"'{self.__class__.__name__}' does not implement 'awake' method."
        raise NotImplementedError(msg)

    @abstractmethod
    def start(self) -> None:
        """Event call on the first frame of the game."""
        msg = f"'{self.__class__.__name__}' does not implement 'start' method."
        raise NotImplementedError(msg)

    @abstractmethod
    def update(self) -> None:
        """Update the component every frame."""
        msg = f"'{self.__class__.__name__}' does not implement 'update' method."
        raise NotImplementedError(msg)

    @abstractmethod
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
        msg = f"'{self.__class__.__name__}' does not implement 'add_events' method."
        raise NotImplementedError(msg)

    def activate(self) -> None:
        """Activate the component."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the component."""
        self.active = False

    def copy(self) -> Self:
        """Create a copy of the game component."""
        """This method should be overridden in subclasses."""
        msg = f"'{self.__class__.__name__}' does not implement 'copy' method."
        raise NotImplementedError(msg)
