"""A render primitive."""

from __future__ import annotations

from typing import TYPE_CHECKING

from harmony.game.material import Material, NoMaterial

if TYPE_CHECKING:
    from harmony.core.assets.sprite_image import SpriteImage
    from harmony.core.packages.geometry.geometry import Geometry


class RenderPrimitive:
    """A render primitive."""

    def __init__(self, material: Material | None = None) -> None:
        """Initialize the RenderPrimitive."""
        self.material = material or NoMaterial()


class GeometryRenderPrimitive(RenderPrimitive):
    """A geometry render primitive."""

    def __init__(self, geometry: Geometry, material: Material | None = None) -> None:
        """Initialize the GeometryRenderPrimitive."""
        super().__init__(material)
        self.geometry = geometry


class SpriteRenderPrimitive(RenderPrimitive):
    """A sprite render primitive."""

    def __init__(self, sprite: SpriteImage, material: Material | None = None) -> None:
        """Initialize the SpriteRenderPrimitive."""
        super().__init__(material)
        self.sprite = sprite
