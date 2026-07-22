"""Game window."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from harmony.core.packages.render.resolution import ResolutionManager


class DisplayMode(Enum):
    """Window display mode."""

    WINDOWED = auto()
    FULLSCREEN = auto()
    BORDERLESS = auto()


@dataclass(slots=True)
class WindowSettings:
    """Window configuration."""

    title: str | None = None
    window_size: tuple[int, int] = (1280, 720)
    world_resolution: tuple[int, int] | None = None
    mode: DisplayMode = DisplayMode.WINDOWED
    resizable: bool = False
    vsync: bool = True


class GameWindow:
    """Game window."""

    def __init__(self, resolution: ResolutionManager, settings: WindowSettings | None = None) -> None:
        """Initialize the game window."""
        self._settings = settings or WindowSettings()
        self._surface: pygame.Surface

        self._resolution = resolution

        self._resolution.set_logical_resolution(self._settings.world_resolution)

        self.apply_settings()

    def apply_settings(self) -> None:
        """Apply the current window settings."""
        flags: int = 0
        window_size = self._settings.window_size

        if self._settings.resizable:
            flags |= pygame.RESIZABLE

        match self._settings.mode:
            case DisplayMode.WINDOWED:
                pass

            case DisplayMode.FULLSCREEN:
                flags |= pygame.FULLSCREEN
                window_size = (0, 0)

            case DisplayMode.BORDERLESS:
                flags |= pygame.NOFRAME
                window_size = (0, 0)

        self._surface = pygame.display.set_mode(
            window_size,
            flags,
            vsync=int(self._settings.vsync),
        )

        if self._settings.title:
            self.set_title(self._settings.title)

    def set_window_size(self, window_size: tuple[int, int]) -> None:
        """Set the window size."""
        self._settings.window_size = window_size
        self.apply_settings()

    def set_mode(self, mode: DisplayMode) -> None:
        """Set the display mode."""
        self._settings.mode = mode
        self.apply_settings()

    def set_title(self, title: str) -> None:
        """Set the window title."""
        self._settings.title = title
        pygame.display.set_caption(title)

    def set_resolution(self, resolution: tuple[int, int]) -> None:
        """Set resolution of the drawing surface."""
        self._resolution.set_logical_resolution(resolution)

    def use_window_size_as_resolution(self) -> None:
        """Set resolution to match window size."""
        self._resolution.set_logical_resolution(None)

    def get_screen_surface(self) -> pygame.Surface:
        """Return the display surface."""
        return self._surface

    def get_logical_surface(self) -> pygame.Surface:
        """Return the logical surface."""
        resolution = self._resolution.get_logical_resolution()
        return pygame.Surface(resolution or self._surface.get_size())

    def get_settings(self) -> WindowSettings:
        """Return the current window settings."""
        return self._settings

    def apply_to_screen(self, surface: pygame.Surface) -> None:
        """Apply the logical surface to the screen surface."""
        self._resolution.apply(surface, self.get_screen_surface())
