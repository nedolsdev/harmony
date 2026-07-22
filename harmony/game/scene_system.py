"""Scene system."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.game.system import System

if TYPE_CHECKING:
    from harmony.game.event_handler import EventHandler
    from harmony.game.scene import Scene
    from harmony.game.scene_manager import SceneManager
    from harmony.game.system_manager import SystemManager


class NoActiveSceneError(RuntimeError):
    """Exception raised when the game tries to run a step but no active scene is set."""


class SceneSystem(System):
    """Scene system."""

    def __init__(self, scene_manager: SceneManager, system_manager: SystemManager, event_handler: EventHandler) -> None:
        """Initialize the SceneSystem."""
        super().__init__()
        self.scene_manager = scene_manager
        self.system_manager = system_manager
        self.event_handler = event_handler

    def update(self) -> None:
        """Update the system."""
        scene_is_unloaded = not self.scene_manager.active_scene_is_loaded()

        scene = self.scene_manager.get_active_scene()
        if scene is None:
            msg = "No active scene exists so the game step has failed."
            raise NoActiveSceneError(msg)

        if scene_is_unloaded:
            self.load_scene(scene)

        objs = scene.get_flattened_game_objects()

        for obj in objs:
            obj.update()

        for obj in objs:
            obj.update_coroutines()

    def load_scene(self, scene: Scene) -> None:
        """Load a given scene."""
        flattened_objs = scene.get_flattened_game_objects()

        for game_object in flattened_objs:
            self.system_manager.component_manager.add_game_object(game_object)
            game_object.add_events(self.event_handler)

        for game_object in flattened_objs:
            game_object.awake()

        for game_object in flattened_objs:
            game_object.start()
