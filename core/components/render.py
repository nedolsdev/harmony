"""A render component is a component that handles the rendering its object."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from game.component import GameComponent

if TYPE_CHECKING:
    import pygame

    from core.components.transform import Transform
    from core.packages.camera.camera_component import Camera


class Render(GameComponent):
    """A render component that can be added to game objects to handle their rendering."""

    @abstractmethod
    def render(self, transform: Transform, surface: pygame.Surface, camera: Camera) -> None:
        """Render the object."""
        msg = f"'{self.__class__.__name__}' does not implement 'render' method."
        raise NotImplementedError(msg)
