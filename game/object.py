"""The object module defines the structure of a game object."""

from typing import TypeVar

from game.component import GameComponent
from game.event_handler import EventHandler

T = TypeVar("T", bound="GameComponent")


class GameObject:
    """A base class for game objects in the game."""

    def __init__(self, event_handler: EventHandler) -> None:
        """Initialize the game object with its components."""
        self.event_handler = event_handler
        self.components: list[GameComponent] = []
        self.tags: set[str] = set()

    def add_component(self, component: GameComponent) -> None:
        """Add a component to the game object."""
        # check if the component is already added
        if self.has_component(type(component)):
            msg = f"Component {type(component).__name__} already exists in the game object."
            raise ValueError(msg)

        self.components.append(component)

    def remove_component(self, component: GameComponent) -> None:
        """Remove a component from the game object."""
        if component in self.components:
            self.components.remove(component)

    def get_components(self) -> list[GameComponent]:
        """Return the list of components attached to the game object."""
        return self.components

    def has_component(self, component_type: type[GameComponent]) -> bool:
        """Check if the game object has a specific component type."""
        return any(isinstance(component, component_type) for component in self.components)

    def get_component(self, component_type: type[T]) -> T:
        """Get a specific component type from the game object."""
        for component in self.components:
            if isinstance(component, component_type):
                return component
        msg = f"Component {component_type.__name__} not found in the game object."
        raise ValueError(msg)
