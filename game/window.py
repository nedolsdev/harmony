"""Game window."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

import pygame


class DisplayMode(Enum):
    """Window display mode."""

    WINDOWED = auto()
    FULLSCREEN = auto()
    BORDERLESS = auto()


@dataclass(slots=True)
class WindowSettings:
    """Window configuration."""

    title: str | None = None
    resolution: tuple[int, int] = (1280, 720)
    mode: DisplayMode = DisplayMode.WINDOWED
    resizable: bool = False
    vsync: bool = True


class GameWindow:
    """Game window."""

    def __init__(self, settings: WindowSettings | None = None) -> None:
        """Initialize the game window."""
        self._settings = settings or WindowSettings()
        self._surface: pygame.Surface

        self.apply_settings()

    def apply_settings(self) -> None:
        """Apply the current window settings."""
        flags: int = 0
        resolution = self._settings.resolution

        if self._settings.resizable:
            flags |= pygame.RESIZABLE

        match self._settings.mode:
            case DisplayMode.WINDOWED:
                pass

            case DisplayMode.FULLSCREEN:
                flags |= pygame.FULLSCREEN
                resolution = (0, 0)

            case DisplayMode.BORDERLESS:
                flags |= pygame.NOFRAME
                resolution = (0, 0)

        self._surface = pygame.display.set_mode(
            resolution,
            flags,
            vsync=int(self._settings.vsync),
        )

        if self._settings.title:
            self.set_title(self._settings.title)

    def set_resolution(self, resolution: tuple[int, int]) -> None:
        """Set the window resolution."""
        self._settings.resolution = resolution
        self.apply_settings()

    def set_mode(self, mode: DisplayMode) -> None:
        """Set the display mode."""
        self._settings.mode = mode
        self.apply_settings()

    def set_title(self, title: str) -> None:
        """Set the window title."""
        self._settings.title = title
        pygame.display.set_caption(title)

    def get_surface(self) -> pygame.Surface:
        """Return the display surface."""
        return self._surface

    def get_settings(self) -> WindowSettings:
        """Return the current window settings."""
        return self._settings
