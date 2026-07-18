"""A render component is a component that handles the rendering its object."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from harmony.game.component import GameComponent

if TYPE_CHECKING:
    import pygame

    from harmony.core.components.transform import Transform
    from harmony.core.packages.camera.camera_component import Camera


class Render(GameComponent, ABC):
    """A render component that can be added to game objects to handle their rendering."""

    @abstractmethod
    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the object."""
