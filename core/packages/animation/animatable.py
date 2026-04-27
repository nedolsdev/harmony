"""An interface for components that can be animated to produce an AnimationClip."""

from __future__ import annotations

from abc import ABC, abstractmethod

from game.component_field import ComponentFields


class Animatable[T: ComponentFields](ABC):
    """An interface for components that can be animated to produce an AnimationClip."""

    @staticmethod
    @abstractmethod
    def get_fields() -> type[T]:
        """Get the field types."""
