"""The movement module defines a behavior that allows an agent to move in the game world."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from core.components.position import Position
from game.behavior import Behavior
from game.event import PygameKeydownEvent

if TYPE_CHECKING:
    from core.objects.grid import Grid
    from game.event_handler import EventHandler


class Movement(Behavior):
    """A behavior that allows an agent to move in the game world."""

    position: Position

    def __init__(self, grid: Grid) -> None:
        """Initialize the movement behavior with an agent and speed."""
        super().__init__()
        self.grid = grid
        self.tile_size = grid.tile_size

    def move_up(self) -> None:
        """Move the agent up by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x, y - 1 * self.grid.tile_size)

    def move_down(self) -> None:
        """Move the agent down by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x, y + 1 * self.grid.tile_size)

    def move_left(self) -> None:
        """Move the agent left by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x - 1 * self.grid.tile_size, y)

    def move_right(self) -> None:
        """Move the agent right by one tile."""
        x, y = self.position.get_coordinates()
        self.try_move(x + 1 * self.grid.tile_size, y)

    def get_position(self) -> tuple[int, int]:
        """Return the agent's current position."""
        return self.position.get_coordinates()

    def move_is_valid(self, x: int, y: int) -> bool:
        """Check if the move to the specified coordinates is valid."""
        return self.grid.on_grid(x, y)

    def try_move(self, x: int, y: int) -> bool:
        """Attempt to move the agent to the specified coordinates."""
        if self.move_is_valid(x // self.grid.tile_size, y // self.grid.tile_size):
            self.position.set_coordinates(x, y)
            return True
        return False

    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.position = self.game_object.get_component(Position)

    def start(self) -> None:
        """Initialize the movement behavior."""

    def update(self) -> None:
        """Update the movement behavior."""

    def add_events(self, event_handler: EventHandler) -> None:
        """Register movement event listeners with the event handler."""
        # add movement listeners
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_UP), self.move_up)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_DOWN), self.move_down)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_LEFT), self.move_left)
        event_handler.register_listener(PygameKeydownEvent.get_name_from_key(pygame.K_RIGHT), self.move_right)

    def copy(self) -> Movement:
        """Create a copy of the movement behavior."""
        new_movement = Movement(self.grid)
        if self.position:
            new_movement.position = self.position.copy()
        return new_movement
