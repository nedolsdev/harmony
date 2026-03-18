"""The object module defines the structure of a game object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, TypeVar

from core.packages.animation.animatable import Animatable
from core.packages.collision.collision_manager import CollisionInteraction

if TYPE_CHECKING:
    from core.packages.animation.frame import AnimationFrame
    from core.packages.collision.collision import Collision
    from game.component import GameComponent
    from game.event_handler import EventHandler

T = TypeVar("T", bound="GameComponent")
U = TypeVar("U")


# custom ObjectAlreadyAwokenError exception
class ObjectAlreadyAwokenError(RuntimeError):
    """Exception raised when a game object has already been awoken."""


# custom ObjectAlreadyStartedError exception
class ObjectAlreadyStartedError(RuntimeError):
    """Exception raised when a game object has already been started."""


class GameObject:
    """A base class for game objects in the game."""

    def __init__(self) -> None:
        """Initialize the game object with its components."""
        self.components: list[GameComponent] = []
        self.tags: set[str] = set()
        self.active = True

        # awoke
        self.awoken = False
        # start
        self.started = False

        # children
        self.children: list[GameObject] = []

        # parent
        self.parent: GameObject | None = None

    def add_component(self, component: GameComponent) -> None:
        """Add a component to the game object."""
        # check if the component is already added
        if not self.is_component_allowed(component):
            msg = f"Component {type(component).__name__} already exists in the game object."
            raise ValueError(msg)

        self.components.append(component)

        # if we have already awoken, now we awake this specific component
        if self.awoken:
            component.awake()

    def is_component_allowed(self, component: GameComponent) -> bool:
        """Check if the component can be added to the game object."""
        return not any(
            component.conflicts_with(existing) or existing.conflicts_with(component) for existing in self.components
        )

    def remove_component(self, component: GameComponent) -> None:
        """Remove a component from the game object."""
        if component in self.components:
            self.components.remove(component)

    def get_components(self) -> list[GameComponent]:
        """Return the list of components attached to the game object."""
        return self.components

    def has_component(self, component_type: type[GameComponent]) -> bool:
        """Check if the game object has a specific component type."""
        return any(component.is_of_type(component_type) for component in self.components)

    def has_exact_component(self, component_type: type[T]) -> bool:
        """Check if the game object has a specific component type (exact match)."""
        return any(component.is_of_exact_type(component_type) for component in self.components)

    def get_component(self, component_type: type[T]) -> T:
        """Get a specific component type from the game object."""
        for component in self.components:
            if isinstance(component, component_type):
                return component
        msg = f"Component {component_type.__name__} not found in the game object."
        raise LookupError(msg)

    def get_components_of_type(self, component_type: type[T]) -> list[T]:
        """Get all components of a specific type from the game object."""
        return [component for component in self.components if isinstance(component, component_type)]

    def get_components_of_any_type(self, component_type: type[U]) -> list[U]:
        """Get all components that satisfy a particular type (where the type is not necessarily a component)."""
        return [component for component in self.components if isinstance(component, component_type)]

    def awake(self) -> None:
        """Event call when the script instance is created."""
        if self.awoken:
            msg = f"GameObject '{self.__class__.__name__}' has already been awoken."
            raise ObjectAlreadyAwokenError(msg)

        self.awoken = True

        for component in self.components:
            component.awake()

    def start(self) -> None:
        """Start the game object by initializing its components."""
        if self.started:
            msg = f"GameObject '{self.__class__.__name__}' has already been started."
            raise ObjectAlreadyStartedError(msg)

        self.started = True

        for component in self.components:
            component.start()

    def update(self) -> None:
        """Update the game object by updating its components."""
        for component in self.components:
            component.update()

    def update_coroutines(self) -> None:
        """Update the coroutines for each component."""
        for component in self.components:
            component.update_coroutines()

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this game object."""
        for component in self.components:
            component.add_events(event_handler)

    def activate(self) -> None:
        """Activate the game object."""
        self.active = True
        for component in self.components:
            component.activate()

    def deactivate(self) -> None:
        """Deactivate the game object."""
        self.active = False
        for component in self.components:
            component.deactivate()

    def copy(self) -> Self:
        """Create a copy of the game object."""
        new_object = type(self)()
        new_object.components = [component.copy() for component in self.components]
        new_object.tags = self.tags.copy()
        new_object.active = self.active
        return new_object

    def add_tag(self, tag: str) -> None:
        """Add a tag to the game object."""
        self.tags.add(tag)

    def add_child(self, child: GameObject) -> None:
        """Add a child game object."""
        self.children.append(child)
        child.parent = self

    def get_children(self) -> list[GameObject]:
        """Return the list of child game objects."""
        return self.children

    def remove_child(self, child: GameObject) -> None:
        """Remove a child game object."""
        if child in self.children:
            self.children.remove(child)
        else:
            msg = f"Child {child.__class__.__name__} not found in the game object's children."
            raise LookupError(msg)

    def get_parent(self) -> GameObject | None:
        """Return the parent game object."""
        return self.parent

    def set_animation_frame(
        self,
        frame: AnimationFrame,
        target: type[GameComponent],
    ) -> None:
        """Set the animation frame to the first component that matches."""
        component = self.get_component(target)

        if not isinstance(component, Animatable):
            msg = f"Tried to animate a component that cannot be animated. Component '{component}'"
            raise TypeError(msg)

        component.set_animation_frame(frame)

    def handle_collision(self, collision: Collision, interaction: CollisionInteraction) -> None:
        """Handle a Collision upon this object."""
        if interaction == CollisionInteraction.ENTER:
            return self.on_collision_enter(collision)
        if interaction == CollisionInteraction.EXIT:
            return self.on_collision_exit(collision)
        return self.on_collision_stay(collision)

    def on_collision_enter(self, collision: Collision) -> None:
        """Send the OnCollisionEnter event to all components."""
        for component in self.components:
            component.on_collision_enter(collision)

    def on_collision_exit(self, collision: Collision) -> None:
        """Send the OnCollisionExit event to all components."""
        for component in self.components:
            component.on_collision_exit(collision)

    def on_collision_stay(self, collision: Collision) -> None:
        """Send the OnCollisionStay event to all components."""
        for component in self.components:
            component.on_collision_stay(collision)
