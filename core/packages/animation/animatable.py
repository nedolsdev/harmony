"""An interface for components that can be animated to produce an AnimationClip."""

from typing import Generic, TypeVar

from core.packages.animation.clip import AnimationFrame

T = TypeVar("T", bound=AnimationFrame)


class Animatable(Generic[T]):
    """An interface for components that can be animated to produce an AnimationClip."""

    def set_animation_frame(self, frame: T) -> None:
        """Set or update the component based on the frame."""
        msg = "The 'set_animation_frame' method should be implemented in subclasses."
        raise NotImplementedError(msg)
