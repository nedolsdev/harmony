"""The game runner module runs the renderer and handles the main game loop."""

import pygame

from game.draw import Renderer
from game.event import Event, PygameEvent, PygameKeydownEvent
from game.event_handler import EventHandler
from world.state import GameState


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
        def quit_listener(_event: Event, _state: GameState) -> None:
            """Stop the game when a quit event is received."""
            self.stop()

        event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        event_handler.register_listener(
            PygameKeydownEvent.get_name_from_key(pygame.K_ESCAPE),
            quit_listener,
        )

    def run_step(self) -> None:
        """Run a single step of the game loop."""
        events: list[Event] = []

        for event in pygame.event.get():
            # check if event is a keydown event
            if event.type == pygame.KEYDOWN:
                events.append(PygameKeydownEvent(event))
            else:
                events.append(PygameEvent(event))

        self.event_handler.handle_events(self.state, events)

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
        while self.running:
            self.run_step()
        pygame.quit()
