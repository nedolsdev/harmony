"""An interface for components that can be animated to produce an AnimationClip."""

from __future__ import annotations

from game.component_field import ComponentFields


class Animatable[T: ComponentFields]:
    """An interface for components that can be animated to produce an AnimationClip."""

    @staticmethod
    def get_fields() -> T:
        """Get the field types."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)
