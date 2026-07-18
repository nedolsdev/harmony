"""Manages different scenes within the game."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.game.lazy_scene import LazyScene
    from harmony.game.scene import Scene


class SceneManager:
    """Manages multiple scenes in the game."""

    def __init__(self) -> None:
        """Initialize the scene manager with no active scene."""
        self.scenes: list[LazyScene] = []
        self.active_scene: LazyScene | None = None

    def add_scene(self, scene: LazyScene) -> None:
        """Add a scene to the manager."""
        self.scenes.append(scene)

    def set_active_scene(self, index: int) -> None:
        """Set the active scene by its index."""
        lazy_scene = self.scenes[index]
        self.active_scene = lazy_scene

    def get_index_of_scene(self, name: str) -> int:
        """Get the index of a scene from its name."""
        for i, scene in enumerate(self.scenes):
            if scene.name == name:
                return i
        msg = f"Could not find scene with name '{name}'"
        raise LookupError(msg)

    def set_active_scene_from_name(self, name: str) -> None:
        """Set the active scene by its name."""
        self.set_active_scene(self.get_index_of_scene(name))

    def reload_active_scene(self) -> None:
        """Reload the active scene if there is one."""
        if self.active_scene is not None:
            self.active_scene.load_scene()

    def get_active_scene(self) -> Scene | None:
        """Get the currently active scene."""
        if self.active_scene is None:
            return None
        return self.active_scene.open_scene()

    def active_scene_is_loaded(self) -> bool:
        """Check if the active scene is already loaded."""
        scene = self.active_scene
        if scene is None:
            return False
        return scene.is_loaded()
