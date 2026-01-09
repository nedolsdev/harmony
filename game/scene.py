"""Represents the current scene of the game, managing game objects within it."""

from typing import TypeVar

from game.object import GameObject, ObjectAlreadyAwokenError

T = TypeVar("T", bound="GameObject")


class Scene:
    """Represents the current scene of the game."""

    def __init__(self, name: str) -> None:
        """Initialize the scene with an empty list of game objects."""
        self.root_objects: list[GameObject] = []
        self.name = name

    def add_game_object(self, game_object: GameObject) -> None:
        """Add a game object to the scene."""
        # check if its awoken
        if game_object.awoken:
            msg = f"GameObject '{game_object.__class__.__name__}' has already been awoken."
            prefab_warn = "Maybe you added the prefab game object to the game state?"
            full_msg = f"{msg} {prefab_warn}"
            raise ObjectAlreadyAwokenError(full_msg)

        self.root_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject) -> None:
        """Remove a game object from the scene."""
        if game_object in self.root_objects:
            self.root_objects.remove(game_object)

    def get_game_objects(self) -> list[GameObject]:
        """Return the list of game objects in the scene."""
        return self.root_objects

    def get_flattened_game_objects(self) -> list[GameObject]:
        """Return a flattened list of all game objects in the scene, including children."""
        all_objects: list[GameObject] = []

        def add_children(obj: GameObject) -> None:
            all_objects.append(obj)
            for child in obj.children:
                add_children(child)

        for root_obj in self.root_objects:
            add_children(root_obj)

        return all_objects

    def find_objects_with_tag(self, tag: str) -> list[GameObject]:
        """Find all game objects with a specific tag within the scene."""
        return [obj for obj in self.get_flattened_game_objects() if tag in obj.tags]

    def find_objects_of_type(self, object_type: type[T]) -> list[T]:
        """Find all game objects of a specific type within the scene."""
        return [obj for obj in self.get_flattened_game_objects() if isinstance(obj, object_type)]
