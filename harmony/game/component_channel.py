"""A channel that exposes all components of a particular type."""

from __future__ import annotations

from harmony.game.component import GameComponent


class ComponentChannel[T: GameComponent]:
    """The ComponentChannel that exposes all components of a particular type."""

    def __init__(self, component_type: type[T]) -> None:
        """Initialize the ComponentChannel."""
        self.component_type = component_type
        self._components: set[T] = set()

    def add_component(self, component: T) -> None:
        """Add a component to the channel."""
        self._components.add(component)

    def remove_component(self, component: T) -> None:
        """Remove a component from the channel."""
        if component not in self._components:
            return
        self._components.remove(component)

    def clear(self) -> None:
        """Clear the channel."""
        self._components: set[T] = set()

    def get_components(self) -> set[T]:
        """Get the components in the channel."""
        return self._components
