"""The game runner module runs the renderer and handles the main game loop."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from harmony.core.packages.timing.delta_time import DeltaTime
from harmony.game.event import PygameEvent, PygameKeyStateEvent
from harmony.game.event_handler import EventHandler
from harmony.game.scene_system import NoActiveSceneError, SceneSystem

if TYPE_CHECKING:
    from harmony.core.packages.render.render_pipeline import RenderPipeline
    from harmony.game.event_backend import EventBackend
    from harmony.game.scene_manager import SceneManager
    from harmony.game.system_manager import SystemManager


class Runner:
    """Runs the game by initializing the renderer and starting the main loop."""

    FPS: int = 60

    def __init__(
        self,
        render_pipeline: RenderPipeline,
        event_backend: EventBackend,
        scene_manager: SceneManager,
        system_manager: SystemManager,
    ) -> None:
        """Initialize the runner with a renderer and an event handler."""
        self.renderer = render_pipeline
        self.clock = pygame.time.Clock()
        self.running = False
        self.scene_manager = scene_manager

        self.event_handler = EventHandler()

        def quit_listener() -> None:
            self.stop()

        self.event_handler.register_listener(PygameEvent.get_name_from_type(pygame.QUIT), quit_listener)
        self.event_handler.register_listener(
            PygameKeyStateEvent.get_name_from_key(pygame.K_ESCAPE, event_type=pygame.KEYDOWN),
            quit_listener,
        )

        self.system_manager = system_manager
        self.system_manager.add_system(SceneSystem(self.scene_manager, self.system_manager, self.event_handler))

        self.delta_time = DeltaTime()

        self.event_backend = event_backend

    def run_step(self) -> None:
        """Run a single step of the game loop."""
        frame_dt: float = self.clock.tick(self.FPS) / 1000.0
        self.delta_time.set(frame_dt)

        # load events
        self.event_backend.poll()
        events = self.event_backend.fetch()

        # pre update
        self.system_manager.pre_update()

        # handle events
        self.event_handler.handle_events(events)
        self.event_backend.clear()

        # update
        self.system_manager.update()

        # post update
        self.system_manager.post_update()

        if not self.running:
            return

        scene = self.scene_manager.get_active_scene()
        if scene is None:
            msg = "No active scene exists so the game step has failed."
            raise NoActiveSceneError(msg)

        self.renderer.draw_frame(scene)

    def stop(self) -> None:
        """Stop the runner."""
        self.running = False

    def start(self) -> None:
        """Start the main game loop."""
        self.system_manager.pre_init()
        self.system_manager.init()

        self.running = True
        self.scene_manager.set_active_scene(0)

        while self.running:
            self.run_step()

        pygame.quit()
