"""Main entry point for the Agent World game."""

from __future__ import annotations

from rich.traceback import install

from example_scenes.animation import create_animation_scene
from example_scenes.collision import create_collision_scene
from example_scenes.input import create_input_scene
from example_scenes.physics import create_physics_scene
from example_scenes.physics_collision import create_physics_collision_scene
from example_scenes.rotation import create_rotation_scene
from example_scenes.sound import create_sound_test_scene
from example_scenes.sprite_sheet import create_sprite_sheet_scene
from example_scenes.tile_map import create_tile_map_scene
from example_scenes.timer import create_timer_scene
from example_scenes.ui import create_ui_scene
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
from harmony.game.image_cache import ImageCache
from harmony.game.lazy_scene import SimpleLazyScene
from harmony.game.logging import EngineLogger
from harmony.game.runner import Runner
from harmony.game.scene_manager import SceneManager
from harmony.game.system_manager import SystemManager
from harmony.game.window import DisplayMode, WindowSettings

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    settings = WindowSettings(mode=DisplayMode.WINDOWED, world_resolution=(750, 750), window_size=(750, 750))

    resolution = ResolutionManager()

    renderer = RenderPipeline(resolution, settings)
    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    scene_manager = SceneManager()

    event_backend = PygameEventBackend()

    system_manager = SystemManager(ComponentManager())
    physics = PhysicsSystem(CollisionManager(), CollisionResolver(), system_manager)
    audio = AudioSystem()
    input_system = InputSystem(InputManager(DeviceManager(PygameDeviceDiscoverer(PygameInputBackend(event_backend)))))

    system_manager.add_system(physics)
    system_manager.add_system(audio)
    system_manager.add_system(input_system)

    game = Runner(renderer, event_backend, scene_manager, system_manager)

    collision_manager = physics.collision_manager

    scenes = [
        SimpleLazyScene(
            "Animation Scene",
            lambda: create_animation_scene(settings, renderer.sorting_layers),
        ),
        SimpleLazyScene(
            "Physics Collision Scene",
            lambda: create_physics_collision_scene(settings, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Physics Scene", lambda: create_physics_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sprite Sheet Scene", lambda: create_sprite_sheet_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene(
            "Input Scene",
            lambda: create_input_scene(settings, renderer.sorting_layers, input_system.input_manager),
        ),
        SimpleLazyScene("UI Scene", lambda: create_ui_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene(
            "Collision Scene",
            lambda: create_collision_scene(settings, renderer.sorting_layers, collision_manager),
        ),
        SimpleLazyScene("Timer Scene", lambda: create_timer_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Sound Scene", lambda: create_sound_test_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Rotation Scene", lambda: create_rotation_scene(settings, renderer.sorting_layers)),
        SimpleLazyScene("Tile Map Scene", lambda: create_tile_map_scene(settings, renderer.sorting_layers)),
    ]

    for scene in scenes:
        scene_manager.add_scene(scene)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
