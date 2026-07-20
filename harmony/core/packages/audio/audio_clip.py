"""Audio clip asset."""

from __future__ import annotations

import pygame

from harmony.game.asset import Asset


class AudioClip(Asset):
    """Audio clip asset."""

    def __init__(self, audio_path: str) -> None:
        """Initialize the AudioClip."""
        super().__init__()
        self.sound = pygame.mixer.Sound(audio_path)
        self.path = audio_path
