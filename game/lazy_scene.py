"""A lazily loaded scene."""
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import override

from game.scene import Scene

type CreateSceneFunc = Callable[[], Scene]


class LazyScene:
    """A lazily loaded scene."""

    def __init__(self, name: str) -> None:
        """Initialize the LazyScene with a name."""
        self.name = name
        self.scene: Scene | None = None

    @abstractmethod
    def _create_scene(self) -> Scene:
        """Get the scene lazily."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def load_scene(self) -> None:
        """Load the scene."""
        self.scene = self._create_scene()

    def open_scene(self) -> Scene:
        """Get the scene, loading it if it doesn't exit."""
        if self.scene is None:
            self.load_scene()
        return self.scene  # pyright: ignore[reportReturnType] (scene was just loaded it can't be None)

    def is_loaded(self) -> bool:
        """Check if the scene is already loaded."""
        return self.scene is not None


class SimpleLazyScene(LazyScene):
    """A lazily loaded scene from a lambda."""

    def __init__(self, name: str, create_func: CreateSceneFunc) -> None:
        """Initialize the LazyScene with a name."""
        super().__init__(name)
        self._create_func = create_func

    @override
    def _create_scene(self) -> Scene:
        """Get the scene lazily."""
        return self._create_func()
