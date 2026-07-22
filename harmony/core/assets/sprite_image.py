"""A SpriteImage Asset."""

from __future__ import annotations

from harmony.game.asset import Asset
from harmony.game.image_cache import ImageCache


class SpriteImage(Asset):
    """A SpriteImage Asset."""

    def __init__(self, image_path: str, size: tuple[int, int] | None = None) -> None:
        """Initialize the sprite image with a file path."""
        self.image_path = image_path
        self.size = size or ImageCache.load(self.image_path).get_size()
        super().__init__()


class SlicedSpriteImage(SpriteImage):
    """A SpriteImage Asset loaded from a portion of a larger asset source."""

    def __init__(self, image_path: str, x: int, y: int, width: int, height: int) -> None:
        """Initialize the sprite image with a file path."""
        super().__init__(image_path, (width, height))
        self.position = (x, y)
