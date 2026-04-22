"""The game runner module runs the renderer and handles the main game loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from core.packages.audio.audio_manager import AudioManager
from core.packages.collision.collision_manager import CollisionManager
from core.packages.collision.collision_resolver import CollisionResolver
from core.packages.input.controls.devices.keyboard import PygameKeyboard
from core.packages.input.controls.devices.mouse import PygameMouse
from core.packages.physics.physics_manager import PhysicsManager
from core.packages.physics.rigidbody_2d import RigidBody2D
from core.packages.timing.delta_time import DeltaTime
from game.behavior import Behavior
from game.event import Event, PygameEvent, PygameKeydownEvent

if TYPE_CHECKING:
    from core.packages.input.input_system import InputSystem
    from game.event_handler import EventHandler
    from game.render_pipeline import RenderPipeline
    from game.scene import Scene
    from game.scene_manager import SceneManager

if TYPE_CHECKING:
    from core.packages.input.controls.device import Device


class NoActiveSceneError(RuntimeError):
    """Exception raised when the game tries to run a step but no active scene is set."""


class Runner:
    """Runs the game by initializing the renderer and starting the main loop."""

    FPS: int = 20
    PHYSICS_TPS: int = 60

    def __init__(
        self,
        render_pipeline: RenderPipeline,
        event_handler: EventHandler,
        scene_manager: SceneManager,
        input_system: InputSystem,
    ) -> None:
        """Initialize the runner with a renderer and an event handler."""
        self.renderer = render_pipeline
        self.event_handler = event_handler
        self.clock = pygame.time.Clock()
        self.running = False
        self.scene_manager = scene_manager

        def quit_listener() -> None:
            self.stop()

        event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_ESCAPE), quit_listener)

        self.delta_time = DeltaTime()

        self.input_system = input_system

        self.keyboard: PygameKeyboard = PygameKeyboard()
        self.mouse: PygameMouse = PygameMouse()
        self.devices: list[Device] = [self.keyboard, self.mouse]

        self.physics = PhysicsManager(
            collision_manager=CollisionManager(),
            collision_resolver=CollisionResolver(),
        )

        self.physics_fixed_dt: float = 1.0 / self.PHYSICS_TPS
        self.physics_accumulator: float = 0.0

    def run_step(self, scene: Scene) -> None:
        """Run a single step of the game loop."""
        frame_dt: float = self.clock.tick(self.FPS) / 1000.0

        # store frame delta separately
        self.delta_time.set(frame_dt)

        self.physics_accumulator += frame_dt

        events: list[Event] = []
        pygame_events = pygame.event.get()

        for event in pygame_events:
            if event.type == pygame.KEYDOWN:
                events.append(PygameKeydownEvent(event))
            else:
                events.append(PygameEvent(event))

        self.event_handler.handle_events(events)

        self.keyboard.events = pygame_events
        self.mouse.events = pygame_events

        self.input_system.update(self.devices)
        AudioManager().update()

        objs = scene.get_flattened_game_objects()

        self.input_system.late_update()

        rigid_bodies: list[RigidBody2D] = [
            obj.get_component(RigidBody2D) for obj in objs if obj.has_component(RigidBody2D)
        ]

        # fixed step physics loop
        steps: int = 0

        while self.physics_accumulator >= self.physics_fixed_dt:
            self.physics.run_physics_step(rigid_bodies, self.physics_fixed_dt)

            for obj in objs:
                obj.fixed_update()

            self.physics_accumulator -= self.physics_fixed_dt
            steps += 1

            if steps >= self.physics.max_physics_steps:
                self.physics_accumulator = 0.0
                break

        for obj in objs:
            obj.update()

        for obj in objs:
            obj.update_coroutines()

        if not self.running:
            return

        self.renderer.draw_frame(scene)

    def stop(self) -> None:
        """Stop the runner."""
        self.running = False

    def load_scene(self, scene: Scene) -> None:
        """Load a given scene."""
        flattened_objs = scene.get_flattened_game_objects()

        for game_object in flattened_objs:
            for component in game_object.get_components():
                if isinstance(component, Behavior):
                    component.set_owner(game_object)

        for game_object in flattened_objs:
            game_object.add_events(self.event_handler)

        for game_object in flattened_objs:
            game_object.awake()

        for game_object in flattened_objs:
            game_object.start()

    def start(self) -> None:
        """Start the main game loop."""
        self.running = True
        self.scene_manager.set_active_scene(0)

        while self.running:
            if not self.scene_manager.active_scene_is_loaded():
                scene = self.scene_manager.get_active_scene()
                if scene is None:
                    msg = "No active scene exists so the game step has failed."
                    raise NoActiveSceneError(msg)
                self.load_scene(scene)

            scene = self.scene_manager.get_active_scene()
            if scene is None:
                msg = "No active scene exists so the game step has failed."
                raise NoActiveSceneError(msg)

            self.run_step(scene)

        pygame.quit()
