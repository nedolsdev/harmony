"""The game runner module runs the renderer and handles the main game loop."""

import pygame

from game.behavior import Behavior
from game.draw import Renderer
from game.event import Event, PygameEvent, PygameKeydownEvent
from game.event_handler import EventHandler
from game.state import GameState


class Runner:
    """Runs the game by initializing the renderer and starting the main loop."""

    FPS = 60

    def __init__(self, renderer: Renderer, event_handler: EventHandler, state: GameState) -> None:
        """Initialize the runner with a renderer and an event handler."""
        self.renderer = renderer
        self.event_handler = event_handler
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = state

        # add game quit listener
        def quit_listener() -> None:
            """Stop the game when a quit event is received."""
            self.stop()

        event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_ESCAPE), quit_listener)

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

        # update all game objects
        for game_object in self.state.get_game_objects():
            game_object.update()

        if not self.running:
            return

        self.renderer.draw_frame(self.state)
        self.clock.tick(self.FPS)

    def stop(self) -> None:
        """Stop the runner."""
        self.running = False

    def start(self) -> None:
        """Start the main game loop."""
        self.running = True

        # set all behavior owners
        for game_object in self.state.get_game_objects():
            for component in game_object.get_components():
                if isinstance(component, Behavior):
                    component.set_owner(game_object)

        # sync all game objects with the event handler
        for game_object in self.state.get_game_objects():
            game_object.add_events(self.event_handler)

        # awake all game objects
        for game_object in self.state.get_game_objects():
            game_object.awake()

        # start all game objects
        for game_object in self.state.get_game_objects():
            game_object.start()

        while self.running:
            self.run_step()
        pygame.quit()
