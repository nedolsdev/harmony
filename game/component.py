"""The component module defines the base class for game components."""

from game.event_handler import EventHandler


class GameComponent:
    """A base class for game components that can be added to the game state."""

    def __init__(self) -> None:
        """Initialize the game component."""
        self.active = True

    def start(self) -> None:
        """Start the component."""
        msg = f"'{self.__class__.__name__}' does not implement 'start' method."
        raise NotImplementedError(msg)

    def update(self) -> None:
        """Update the component."""
        msg = f"'{self.__class__.__name__}' does not implement 'update' method."
        raise NotImplementedError(msg)

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
