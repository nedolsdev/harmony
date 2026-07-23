"""A Tile is a cell of a TileMap."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.core.packages.render.primitive import SurfaceRenderPrimitive


class Tile:
    """A tile holds the base render primitive for a tile map cell."""

    def __init__(self, primitive: SurfaceRenderPrimitive) -> None:
        """Initialize the Tile."""
        self.primitive = primitive
