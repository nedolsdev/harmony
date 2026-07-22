"""ComponentManager manages all the component channels."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.game.behavior import Behavior
from harmony.game.component import GameComponent
from harmony.game.component_channel import ComponentChannel

if TYPE_CHECKING:
    from harmony.game.object import GameObject


class ComponentManager:
    """ComponentManager manages all the component channels."""

    def __init__(self) -> None:
        """Initialize the ComponentManager."""
        self._channels: dict[type[GameComponent], ComponentChannel] = {}

    def has_channel(self, component_type: type[GameComponent]) -> bool:
        """Check if the ComponentManager has a channel for this component."""
        return self._channels.get(component_type, None) is not None

    def add_channel[T: GameComponent](self, component_type: type[T]) -> ComponentChannel[T]:
        """Add a channel if it doesn't exist yet for a particular component type."""
        channel = self.get_channel(component_type)
        if channel is not None:
            return channel

        channel = ComponentChannel(component_type)
        self._channels[component_type] = channel
        return channel

    def remove_channel(self, component_type: type[GameComponent]) -> None:
        """Remove a channel for a particular component type."""
        self._channels.pop(component_type, None)

    def get_channel[T: GameComponent](self, component_type: type[T]) -> ComponentChannel[T] | None:
        """Get a channel for a particular component type."""
        return self._channels.get(component_type, None)

    def add_game_object(self, game_object: GameObject) -> None:
        """Add all the components for a game object to their channels."""
        for component in game_object.get_components():
            if isinstance(component, Behavior):
                component.set_owner(game_object)
            self.add_component(component)

    def remove_game_object(self, game_object: GameObject) -> None:
        """Remove all the components for a game object from their channels."""
        for component in game_object.get_components():
            self.remove_component(component)

    def add_component(self, component: GameComponent) -> None:
        """Add a component to a channel."""
        channel = self.add_channel(type(component))
        channel.add_component(component)

    def remove_component(self, component: GameComponent) -> None:
        """Remove a component from a channel."""
        channel = self.add_channel(type(component))
        channel.remove_component(component)

    def get_components_of_type[T: GameComponent](self, component_type: type[T]) -> set[T]:
        """Get components of a particular type."""
        channel = self.get_channel(component_type)
        if channel is None:
            return set()
        return channel.get_components()
