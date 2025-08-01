"""A material module that defines a simple material class for rendering."""

import pygame


class Material:
    """The base material class for render components."""

    def apply(self, surface: "pygame.Surface") -> None:
        """Apply the material to the given surface."""
        msg = f"'{self.__class__.__name__}' does not implement 'apply' method."
        raise NotImplementedError(msg)


class MaterialStack(Material):
    """A stack of materials that can be applied in sequence."""

    def __init__(self) -> None:
        """Initialize an empty material stack."""
        self.materials: list[Material] = []

    def add_material(self, material: Material) -> None:
        """Add a material to the stack."""
        self.materials.append(material)

    def apply(self, surface: "pygame.Surface") -> None:
        """Apply all materials in the stack to the given surface."""
        for material in self.materials:
            material.apply(surface)


class ColorMaterial(Material):
    """A simple material class to hold color information."""

    def __init__(self, color: tuple[int, int, int], alpha: int = 255) -> None:
        """Initialize the color material with RGB color and alpha."""
        self.color = color
        self.alpha = alpha

    def apply(self, surface: "pygame.Surface") -> None:
        """Apply the color material to the given surface."""
        surface.fill((*self.color, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
