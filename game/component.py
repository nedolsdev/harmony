"""The component module defines the base class for game components."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Self, TypeVar

from core.packages.timing.coroutine_manager import CoroutineManager

if TYPE_CHECKING:
    from core.packages.collision.collision import Collision
    from core.packages.timing.coroutine import Coroutine
    from game.event_handler import EventHandler

T = TypeVar("T", bound="GameComponent")


class GameComponent:
    """A base class for game components that can be added to the game state."""

    def __init__(
        self,
        *args,  # noqa: ANN002
        disallow_multiple_of_type: bool = False,
        disallow_multiple_of_exact_type: bool = False,
        **kwargs,  # noqa: ANN003
    ) -> None:
        """Initialize the game component."""
        super().__init__(*args, **kwargs)

        self.active = True

        self.disallow_multiple_of_type = disallow_multiple_of_type
        self.disallow_multiple_of_exact_type = disallow_multiple_of_exact_type

        self.coroutine_manager = CoroutineManager()

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

    @abstractmethod
    def fixed_update(self) -> None:
        """Update the component in the physics / fixed loop."""
        msg = f"'{self.__class__.__name__}' does not implement 'fixed_update' method."
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

    def is_of_type(self, component_type: type[T]) -> bool:
        """Check if the component is of a specific type."""
        return isinstance(self, component_type)

    def is_of_exact_type(self, component_type: type[T]) -> bool:
        """Check if the component is of a specific type (exact match)."""
        return type(self) is component_type

    def conflicts_with(self, other: GameComponent) -> bool:
        """Check if this component conflicts with another component."""
        return (self.disallow_multiple_of_type and other.is_of_type(type(self))) or (
            self.disallow_multiple_of_exact_type and other.is_of_exact_type(type(self))
        )

    def update_coroutines(self) -> None:
        """Update the component's coroutines."""
        self.coroutine_manager.update()

    def start_coroutine(self, coroutine: Coroutine) -> None:
        """Start a given coroutine."""
        self.coroutine_manager.start(coroutine)

    def on_collision_enter(self, collision: Collision) -> None:
        """Send the OnCollisionEnter event to all components."""

    def on_collision_exit(self, collision: Collision) -> None:
        """Send the OnCollisionExit event to all components."""

    def on_collision_stay(self, collision: Collision) -> None:
        """Send the OnCollisionStay event to all components."""
