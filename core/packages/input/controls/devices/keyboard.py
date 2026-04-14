"""A basic keyboard device."""
from __future__ import annotations

from typing import override

import pygame

from core.packages.input.controls.device import Device, DeviceType


class Keyboard(Device):
    """A basic keyboard device."""

    def __init__(self) -> None:
        """Initialize the Keyboard."""
        super().__init__(device_type=DeviceType.KEYBOARD)
        self.key_state: dict[int, bool] = {}


class PygameKeyboard(Keyboard):
    """A simple Keyboard that reads key states from pygame events."""

    def __init__(self) -> None:
        """Initialize the PygameKeyboard."""
        super().__init__()
        self.events: list[pygame.Event] = []

    @override
    def update(self) -> None:
        """Update the key states."""
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.key_state[event.key] = True
            elif event.type == pygame.KEYUP:
                self.key_state[event.key] = False
