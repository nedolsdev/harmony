"""A basic keyboard device."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import pygame

from core.packages.input.controls.device import Device, DeviceType
from game.event import PygameKeyStateEvent

if TYPE_CHECKING:
    from core.packages.input.input_backend import InputBackend, PygameInputBackend


class Keyboard(Device):
    """A basic keyboard device."""

    def __init__(self, input_backend: InputBackend) -> None:
        """Initialize the Keyboard."""
        super().__init__(device_type=DeviceType.KEYBOARD, input_backend=input_backend)
        self.key_state: dict[int, bool] = {}


class PygameKeyboard(Keyboard):
    """A simple Keyboard that reads key states from pygame events."""

    def __init__(self, pygame_backend: PygameInputBackend) -> None:
        """Initialize the PygameKeyboard."""
        super().__init__(input_backend=pygame_backend)
        self.input_backend: PygameInputBackend

    @override
    def update(self) -> None:
        """Update the key states."""
        for event in self.input_backend.events:
            if isinstance(event, PygameKeyStateEvent):
                if event.pygame_type == pygame.KEYDOWN:
                    self.key_state[event.key] = True
                elif event.pygame_type == pygame.KEYUP:
                    self.key_state[event.key] = False
