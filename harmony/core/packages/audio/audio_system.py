"""Audio system."""

from __future__ import annotations

import pygame

from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.game.system import System


class AudioSystem(System):
    """Audio system."""

    def __init__(self) -> None:
        """Initialize the Audio System."""
        super().__init__()

    def pre_init(self) -> None:
        """Pre-init the system."""
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        AudioManager(number_of_channels=32)

    def pre_update(self) -> None:
        """Pre-update the system."""
        AudioManager().update()
