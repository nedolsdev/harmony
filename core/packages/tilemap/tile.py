"""A Tile is a cell of a TileMap."""

from core.assets.sprite_image import SpriteImage


class Tile(SpriteImage):
    """A Tile is a cell of a TileMap."""

    def __init__(self, image_path: str) -> None:
        """Initialize the Tile with a sprite image."""
        super().__init__(image_path)
