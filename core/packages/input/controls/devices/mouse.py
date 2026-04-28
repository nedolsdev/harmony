"""A basic mouse device."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.packages.input.controls.device import Device, DeviceType
from game.event import PygameMouseMoveEvent, PygameMouseStateEvent, PygameMouseWheelEvent

if TYPE_CHECKING:
    from core.packages.input.input_backend import InputBackend, PygameInputBackend


class Mouse(Device):
    """A basic mouse device."""

    def __init__(self, input_backend: InputBackend) -> None:
        """Initialize the Mouse."""
        super().__init__(device_type=DeviceType.MOUSE, input_backend=input_backend)
        self.button_state: dict[int, bool] = {}
        self.position: tuple[int, int] = (0, 0)
        self.relative: tuple[int, int] = (0, 0)
        self.scroll: tuple[int, int] = (0, 0)


class PygameMouse(Mouse):
    """A simple Mouse that reads state from pygame events."""

    def __init__(self, pygame_backend: PygameInputBackend) -> None:
        """Initialize the PygameMouse."""
        super().__init__(input_backend=pygame_backend)
        self.input_backend: PygameInputBackend

    @override
    def update(self) -> None:
        """Update the mouse state."""
        self.relative = (0, 0)
        self.scroll = (0, 0)

        for event in self.input_backend.events:
            if isinstance(event, PygameMouseStateEvent):
                if event.pygame_type == pygame.MOUSEBUTTONDOWN:
                    self.button_state[event.button] = True

                elif event.pygame_type == pygame.MOUSEBUTTONUP:
                    self.button_state[event.button] = False

            if isinstance(event, PygameMouseMoveEvent):
                self.position = event.pos
                self.relative = event.rel

            if isinstance(event, PygameMouseWheelEvent):
                self.scroll = (event.x, event.y)
