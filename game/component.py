"""The component module defines the base class for game components."""


class GameComponent:
    """A base class for game components that can be added to the game state."""

    def __init__(self) -> None:
        """Initialize the game component."""
        self.active = True
