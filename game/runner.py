"""The game runner module runs the renderer and handles the main game loop."""

from typing import TYPE_CHECKING

import pygame

from core.packages.audio.audio_manager import AudioManager
from core.packages.input.controls.devices.keyboard import PygameKeyboard
from core.packages.input.controls.devices.mouse import PygameMouse
from core.packages.input.input_system import InputSystem
from core.packages.timing.delta_time import DeltaTime
from game.behavior import Behavior
from game.event import Event, PygameEvent, PygameKeydownEvent
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

    FPS = 60

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

        # add game quit listener
        def quit_listener() -> None:
            """Stop the game when a quit event is received."""
            self.stop()

        event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_ESCAPE), quit_listener)

        # delta time
        self.delta_time = DeltaTime()

        # inputs
        self.input_system = input_system

        # basic pygame devices (maybe temp)
        self.keyboard: PygameKeyboard = PygameKeyboard()
        self.mouse: PygameMouse = PygameMouse()

        # devices
        self.devices: list[Device] = [self.keyboard, self.mouse]

    def run_step(self, scene: Scene) -> None:
        """Run a single step of the game loop."""
        events: list[Event] = []

        pygame_events = pygame.event.get()

        for event in pygame_events:
            # check if event is a keydown event
            if event.type == pygame.KEYDOWN:
                key_down_event = PygameKeydownEvent(event)
                events.append(key_down_event)
            else:
                events.append(PygameEvent(event))

        self.event_handler.handle_events(events)

        # TODO: Refactor this out later  # noqa: TD003
        self.keyboard.events = pygame_events
        self.mouse.events = pygame_events
        # update the inputs
        self.input_system.update(self.devices)

        # update audio manager
        AudioManager().update()

        # update collisions
        scene.collision_manager.update()

        # update all game objects
        objs = scene.get_flattened_game_objects()

        for game_object in objs:
            game_object.update()

        for game_object in objs:
            game_object.update_coroutines()

        # late update
        self.input_system.late_update()

        if not self.running:
            return

        self.renderer.draw_frame(scene)
        dt = self.clock.tick(self.FPS) / 1000.0
        self.delta_time.set(dt)

    def stop(self) -> None:
        """Stop the runner."""
        self.running = False

    def load_scene(self, scene: Scene) -> None:
        """Load a given scene."""
        flattened_objs = scene.get_flattened_game_objects()

        # set all behavior owners
        for game_object in flattened_objs:
            for component in game_object.get_components():
                if isinstance(component, Behavior):
                    component.set_owner(game_object)

        # sync all game objects with the event handler
        for game_object in flattened_objs:
            game_object.add_events(self.event_handler)

        # awake all game objects
        for game_object in flattened_objs:
            game_object.awake()

        # start all game objects
        for game_object in flattened_objs:
            game_object.start()

    def start(self) -> None:
        """Start the main game loop."""
        self.running = True

        # choose the first scene
        self.scene_manager.set_active_scene(0)

        while self.running:
            loaded = self.scene_manager.active_scene_is_loaded()

            scene = self.scene_manager.get_active_scene()

            if scene is None:
                msg = "No active scene exists so the game step has failed."
                raise NoActiveSceneError(msg)

            if not loaded:
                self.load_scene(scene)

            self.run_step(scene)

        pygame.quit()
