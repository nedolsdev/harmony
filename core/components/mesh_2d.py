"""The 2D mesh component for the Agent World game."""

from game.component import GameComponent
from game.event_handler import EventHandler


class Material:
    """A simple material class to hold color information."""

    def __init__(self, color: tuple[int, int, int]) -> None:
        """Initialize the material with a color."""
        self.color = color


class Mesh2D(GameComponent):
    """A 2D mesh component for the Agent World game."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the 2D mesh with given width and height."""
        super().__init__()
        self.width = width
        self.height = height
        self.material = Material((43, 150, 243))  # Default color

    def get_dimensions(self) -> tuple[int, int]:
        """Return the width and height of the mesh."""
        return self.width, self.height

    def set_dimensions(self, width: int, height: int) -> None:
        """Set the width and height of the mesh."""
        self.width = width
        self.height = height

    def start(self) -> None:
        """Initialize the mesh component."""

    def update(self) -> None:
        """Update the mesh component."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""
