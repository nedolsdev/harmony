"""Audio system."""

from __future__ import annotations

from harmony.core.packages.audio.audio_manager import AudioManager
from harmony.game.system import System


class AudioSystem(System):
    """Audio system."""

    def __init__(self) -> None:
        """Initialize the Audio System."""
        super().__init__()

    def pre_update(self) -> None:
        """Pre-update the system."""
        AudioManager().update()
