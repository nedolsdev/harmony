"""The component module defines the base class for game components."""


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
