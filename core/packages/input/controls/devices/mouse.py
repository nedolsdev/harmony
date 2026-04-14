"""A basic mouse device."""

from typing import override

import pygame

from core.packages.input.controls.device import Device, DeviceType


class Mouse(Device):
    """A basic mouse device."""

    def __init__(self) -> None:
        """Initialize the Mouse."""
        super().__init__(device_type=DeviceType.MOUSE)
        self.button_state: dict[int, bool] = {}
        self.position: tuple[int, int] = (0, 0)
        self.relative: tuple[int, int] = (0, 0)
        self.scroll: tuple[int, int] = (0, 0)


class PygameMouse(Mouse):
    """A simple Mouse that reads state from pygame events."""

    def __init__(self) -> None:
        """Initialize the PygameMouse."""
        super().__init__()
        self.events: list[pygame.Event] = []

    @override
    def update(self) -> None:
        """Update the mouse state."""
        self.relative = (0, 0)
        self.scroll = (0, 0)

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button_state[event.button] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_state[event.button] = False

            elif event.type == pygame.MOUSEMOTION:
                self.position = event.pos
                self.relative = event.rel

            elif event.type == pygame.MOUSEWHEEL:
                self.scroll = (event.x, event.y)
