"""A render component is a component that handles the rendering its object."""

from abc import abstractmethod

import pygame

from core.components.position import Position
from core.components.rotation import Rotation
from game.component import GameComponent


class Render(GameComponent):
    """A render component that can be added to game objects to handle their rendering."""

    @abstractmethod
    def render(self, position: Position, surface: pygame.Surface, *, rotation: Rotation | None = None) -> None:
        """Render the object."""
        msg = f"'{self.__class__.__name__}' does not implement 'render' method."
        raise NotImplementedError(msg)
