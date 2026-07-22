"""Simple runner with sensible defaults."""

from __future__ import annotations

from harmony.core.packages.audio.audio_system import AudioSystem
from harmony.core.packages.collision.collision_manager import CollisionManager
from harmony.core.packages.collision.collision_resolver import CollisionResolver
from harmony.core.packages.input.device_discoverer import PygameDeviceDiscoverer
from harmony.core.packages.input.device_manager import DeviceManager
from harmony.core.packages.input.input_backend import PygameInputBackend
from harmony.core.packages.input.input_manager import InputManager
from harmony.core.packages.input.input_system import InputSystem
from harmony.core.packages.physics.physics_manager import PhysicsSystem
from harmony.core.packages.render.render_pipeline import RenderPipeline
from harmony.core.packages.render.resolution import ResolutionManager
from harmony.game.component_manager import ComponentManager
from harmony.game.event_backend import PygameEventBackend
from harmony.game.runner import Runner
from harmony.game.scene_manager import SceneManager
from harmony.game.system_manager import SystemManager
from harmony.game.window import WindowSettings


class SimpleRunner(Runner):
    """Simple runner with sensible defaults."""

    def __init__(self, settings: WindowSettings | None = None) -> None:
        """Initialize the SimpleRunner."""
        event_backend = PygameEventBackend()
        super().__init__(
            RenderPipeline(ResolutionManager(), settings or WindowSettings()),
            event_backend,
            SceneManager(),
            SystemManager(
                ComponentManager(),
            ),
        )

        self.physics = PhysicsSystem(CollisionManager(), CollisionResolver(), self.system_manager)
        self.input_system = InputSystem(
            InputManager(DeviceManager(PygameDeviceDiscoverer(PygameInputBackend(event_backend)))),
        )

        self.system_manager.add_system(self.physics)
        self.system_manager.add_system(AudioSystem())
        self.system_manager.add_system(self.input_system)

        self.renderer.sorting_layers.create_layer("Background", 0)
        self.renderer.sorting_layers.create_layer("Default", 10)
        self.renderer.sorting_layers.create_layer("UI", 100)
