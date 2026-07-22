"""A render component is a component that handles the rendering its object."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from harmony.game.component import GameComponent

if TYPE_CHECKING:
    from harmony.core.components.transform import Transform
    from harmony.core.packages.render.primitive import RenderPrimitive


class Render(GameComponent, ABC):
    """A render component that can be added to game objects to handle their rendering."""

    @abstractmethod
    def render(self, transform: Transform) -> list[RenderPrimitive]:
        """Render the object at the world position."""
