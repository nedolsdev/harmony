"""The prefab module defines the prefab class for the game."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from game.behavior import Behavior
from game.object import GameObject

if TYPE_CHECKING:
    from game.component import GameComponent

T = TypeVar("T", bound=GameObject)


class Prefab[T: GameObject]:
    """A prefab is a reusable game object template."""

    def __init__(self, game_object: T) -> None:
        """Initialize the prefab with a game object."""
        self.game_object = game_object

        for component in game_object.get_components():
            if isinstance(component, Behavior):
                component.set_owner(game_object)

        # NOTE: we need to call awake so that we can copy it correctly to create new instances
        # this means that we cannot use the game object as both as a prefab and a game object in the game state
        # because it is already awake. However, you probably should not do that anyway.
        self.game_object.awake()

    def instantiate(self) -> T:
        """Create a new instance of the prefab. Used when the game has already started."""
        game_object = self.create_object()
        game_object.awake()
        return game_object

    def instantiate_with(self, components: list[GameComponent]) -> T:
        """Create a new instance of the prefab with additional components. Used when the game has already started."""
        game_object = self.create_object()
        for component in components:
            # if we have already have the component, remove it
            if game_object.has_exact_component(type(component)):
                game_object.remove_component(game_object.get_component(type(component)))
            game_object.add_component(component)
        game_object.awake()
        return game_object

    def create_object(self) -> T:
        """Create a new instance of the prefab's game object. Used when the game has not started yet."""
        game_object = self.game_object.copy()

        for component in self.game_object.get_components():
            if isinstance(component, Behavior):
                component.set_owner(game_object)

        return game_object
