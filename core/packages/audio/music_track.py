"""Music track asset."""

from game.asset import Asset


class MusicTrack(Asset):
    """Music track asset."""

    def __init__(self, path: str) -> None:
        """Initialize the AudioClip."""
        super().__init__()
        self.path = path
