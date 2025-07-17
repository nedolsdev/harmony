"""The movement module defines a behavior that allows an agent to move in the game world."""

import pygame

from core.components.position import Position
from core.objects.grid import Grid
from game.behavior import Behavior
from game.event import PygameKeydownEvent
from game.event_handler import EventHandler


class Movement(Behavior):
    """A behavior that allows an agent to move in the game world."""

    position: Position

    def __init__(self, grid: Grid) -> None:
        """Initialize the movement behavior with an agent and speed."""
        super().__init__()
        self.grid = grid

    def move_up(self) -> None:
        """Move the agent up by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x, y - 1)

    def move_down(self) -> None:
        """Move the agent down by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x, y + 1)

    def move_left(self) -> None:
        """Move the agent left by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x - 1, y)

    def move_right(self) -> None:
        """Move the agent right by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x + 1, y)

    def get_position(self) -> tuple[int, int]:
        """Return the agent's current position."""
        return self.position.get_coordinates()

    def move_is_valid(self, x: int, y: int) -> bool:
        """Check if the move to the specified coordinates is valid."""
        return self.grid.on_grid(x, y)

    def try_move(self, x: int, y: int) -> bool:
        """Attempt to move the agent to the specified coordinates."""
        if self.move_is_valid(x, y):
            self.position.set_coordinates(x, y)
            return True
        return False

    def start(self) -> None:
        """Initialize the movement behavior."""
        self.position = self.game_object.get_component(Position)

    def update(self) -> None:
        """Update the movement behavior."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Register movement event listeners with the event handler."""
        # add movement listeners
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_UP), self.move_up)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_DOWN), self.move_down)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_LEFT), self.move_left)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_RIGHT), self.move_right)
