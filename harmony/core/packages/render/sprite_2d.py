"""The 2D sprite component."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from harmony.core.packages.geometry.rectangle import Rectangle
from harmony.core.packages.geometry.transform import transform_rectangle
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.render.primitive import RenderPrimitive, SpriteRenderPrimitive
from harmony.core.packages.render.render import Render
from harmony.game.material import NoMaterial

if TYPE_CHECKING:
    from harmony.core.assets.sprite_image import SpriteImage
    from harmony.core.components.transform import Transform
    from harmony.game.event_handler import EventHandler
    from harmony.game.material import Material


class Sprite2D(Render):
    """A 2D sprite component."""

    def __init__(self, image: SpriteImage, material: Material | None = None) -> None:
        """Initialize the 2D sprite with given width and height."""
        super().__init__()
        self.image = image
        self.material = material or NoMaterial()
        local_size = image.true_pixel_size * image.scale
        width, height = local_size.as_tuple()
        self.rect = Rectangle(width, height, center=Vector2.zero())

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def late_update(self) -> None:
        """Late update the component every frame."""

    @override
    def fixed_update(self) -> None:
        """Update the sprite component in the physics / fixed loop."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
        return [
            SpriteRenderPrimitive(
                self.image,
                transform_rectangle(self.rect, transform),
            ),
        ]

    def copy(self) -> Sprite2D:
        """Create a copy of the sprite component."""
        return Sprite2D(self.image, self.material)
