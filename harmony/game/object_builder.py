"""The object builder module defines the base class for a GameObject builder."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, TypeVar

from harmony.game.error import DataAlreadyExistsError
from harmony.game.object import GameObject
from harmony.game.prefab import Prefab

if TYPE_CHECKING:
    from harmony.game.component import GameComponent

T = TypeVar("T", bound=GameObject)


class GameObjectBuilder[T: GameObject]:
    """A base class for building game objects."""

    def __init__(self, t: type[T]) -> None:
        """Initialize the object builder."""
        self._type = t
        self._tags: set[str] = set()
        self._components: list[GameComponent] = []

    def build(self) -> T:
        """Build and return the game object."""
        game_object = self.create_game_object()
        for component in self._components:
            game_object.add_component(component)
        for tag in self._tags:
            game_object.add_tag(tag)
        return game_object

    def build_as_prefab(self) -> Prefab[T]:
        """Build and return the prefab of the game object."""
        game_object = self.build()
        return Prefab(game_object)

    def create_game_object(self) -> T:
        """Create a new instance of the game object."""
        return self._type()

    def add_tag(self, tag: str) -> Self:
        """Add a tag to the game object."""
        self._tags.add(tag)
        return self

    def add_component(self, component: GameComponent) -> Self:
        """Add a component to the game object."""
        if component in self._components:
            msg = f"Component {type(component).__name__} already exists in the game object."
            raise DataAlreadyExistsError(msg)
        self._components.append(component)
        return self
