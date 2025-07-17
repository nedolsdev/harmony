"""The object module defines the structure of a game object."""

from typing import TypeVar

from game.component import GameComponent
from game.event_handler import EventHandler

T = TypeVar("T", bound="GameComponent")


class GameObject:
    """A base class for game objects in the game."""

    def __init__(self) -> None:
        """Initialize the game object with its components."""
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

    def start(self) -> None:
        """Start the game object by initializing its components."""
        for component in self.components:
            component.start()

    def update(self) -> None:
        """Update the game object by updating its components."""
        for component in self.components:
            component.update()

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this game object."""
        msg = f"'{self.__class__.__name__}' does not implement 'add_events' method."
        raise NotImplementedError(msg)
