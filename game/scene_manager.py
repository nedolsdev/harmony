"""Manages different scenes within the game."""

from game.scene import Scene


class SceneManager:
    """Manages multiple scenes in the game."""

    def __init__(self) -> None:
        """Initialize the scene manager with no active scene."""
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene | None = None

    def add_scene(self, scene: Scene) -> None:
        """Add a scene to the manager."""
        self.scenes[scene.name] = scene

    def set_active_scene(self, scene_name: str) -> None:
        """Set the active scene by its name."""
        scene = self.scenes.get(scene_name)
        if scene is None:
            msg = f"Scene with name '{scene_name}' does not exist."
            raise ValueError(msg)
        self.active_scene = scene

    def get_active_scene(self) -> Scene | None:
        """Get the currently active scene."""
        return self.active_scene
