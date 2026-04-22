"""A component field is a data source that can be targeted by an animation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from core.packages.animation.frame import AnimationFrame
    from game.component import GameComponent


@dataclass(frozen=True)
class ComponentField[T: AnimationFrame, U: GameComponent]:
    """A component field is a data source that can be targeted by an animation."""

    update: Callable[[U, T], None]
    component_type: type[U]


@dataclass(frozen=True)
class ComponentFields:
    """A set of component fields that can be targeted by an animation."""
