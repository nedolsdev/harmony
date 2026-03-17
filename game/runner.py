"""The game runner module runs the renderer and handles the main game loop."""

import pygame

from core.packages.audio.audio_manager import AudioManager
from core.packages.collision.collision_manager import CollisionManager
from core.packages.timing.delta_time import DeltaTime
from game.behavior import Behavior
from game.event import Event, PygameEvent, PygameKeydownEvent
from game.event_handler import EventHandler
from game.render_pipeline import RenderPipeline
from game.scene import Scene


class Runner:
    """Runs the game by initializing the renderer and starting the main loop."""

    FPS = 60

    def __init__(self, render_pipeline: RenderPipeline, event_handler: EventHandler, scene: Scene) -> None:
        """Initialize the runner with a renderer and an event handler."""
        self.renderer = render_pipeline
        self.event_handler = event_handler
        self.clock = pygame.time.Clock()
        self.running = False
        self.scene = scene

        # add game quit listener
        def quit_listener() -> None:
            """Stop the game when a quit event is received."""
            self.stop()

        event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_ESCAPE), quit_listener)

        # delta time
        self.delta_time = DeltaTime()

        # collisions
        self.collision_manager = CollisionManager()

    def run_step(self) -> None:
        """Run a single step of the game loop."""
        events: list[Event] = []

        for event in pygame.event.get():
            # check if event is a keydown event
            if event.type == pygame.KEYDOWN:
                events.append(PygameKeydownEvent(event))
            else:
                events.append(PygameEvent(event))

        self.event_handler.handle_events(events)

        # update audio manager
        AudioManager().update()

        # update collisions
        self.collision_manager.update()

        # update all game objects
        objs = self.scene.get_flattened_game_objects()

        for game_object in objs:
            game_object.update()

        for game_object in objs:
            game_object.update_coroutines()

        if not self.running:
            return

        self.renderer.draw_frame(self.scene)
        dt = self.clock.tick(self.FPS) / 1000.0
        self.delta_time.set(dt)

    def stop(self) -> None:
        """Stop the runner."""
        self.running = False

    def start(self) -> None:
        """Start the main game loop."""
        self.running = True

        flattened_objs = self.scene.get_flattened_game_objects()

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

        while self.running:
            self.run_step()
        pygame.quit()
