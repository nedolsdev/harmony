"""A simple sprite sheet implementation."""

from __future__ import annotations

from abc import abstractmethod
from typing import override

from core.assets.sprite_image import SlicedSpriteImage, SpriteImage


class SpriteSheet(SpriteImage):
    """Base sprite sheet asset."""

    def __init__(self, image_path: str) -> None:
        """Initialize the SpriteSheet asset."""
        super().__init__(image_path)
        self.sprites: list[int] = []

    @abstractmethod
    def get_sprites(self) -> list[SlicedSpriteImage]:
        """Get the individual sprites from the sprite asset."""
        raise NotImplementedError

    @abstractmethod
    def get_sprite(self, sprite_id: int) -> SlicedSpriteImage:
        """Get the sprite by its id in the sprite sheet."""
        raise NotImplementedError


class SimpleSpriteSheet(SpriteSheet):
    """A simple sprite sheet asset with a grid-layout."""

    def __init__(self, image_path: str, sprite_width: int, sprite_height: int, *, grid_gap: int = 0) -> None:
        """Initialize the SimpleSpriteSheet asset."""
        super().__init__(image_path)
        self._width = sprite_width
        self._height = sprite_height
        self._grid_gap = grid_gap

    @override
    def get_sprites(self) -> list[SlicedSpriteImage]:
        image_width, image_height = self.get_size()

        step_x = self._width + self._grid_gap
        step_y = self._height + self._grid_gap

        columns = (image_width + self._grid_gap) // step_x
        rows = (image_height + self._grid_gap) // step_y

        return [self.get_sprite(i) for i in range(rows * columns)]

    @override
    def get_sprite(self, sprite_id: int) -> SlicedSpriteImage:
        image_width, _ = self.get_size()
        step_x = self._width + self._grid_gap
        step_y = self._height + self._grid_gap

        columns = (image_width + self._grid_gap) // step_x

        row = sprite_id // columns
        column = sprite_id % columns
        x = column * step_x
        y = row * step_y

        return SlicedSpriteImage(
            self.image_path,
            x,
            y,
            self._width,
            self._height,
        )
