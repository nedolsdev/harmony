"""An interface for components that can be animated to produce an AnimationClip."""

from typing import Generic, Self, TypeVar

from core.components.position import Position
from core.packages.animation.clip import AnimationFrame, SimpleAnimationClip
from core.packages.animation.frame import VectorFrame

T = TypeVar("T", bound=AnimationFrame)


class AnimationBuilder(Generic[T]):
    """A helper for creating animations."""

    def __init__(self, fps: int) -> None:
        """Initialize the AnimationBuilder with FPS."""
        self.clip = SimpleAnimationClip(fps)

    def export(self) -> SimpleAnimationClip:
        """Export the animation clip."""
        return self.clip

    def add_frame(self, frame: T) -> Self:
        """Add a frame to the animation."""
        self.clip.add_frame(frame)
        return self


class Animatable(Generic[T]):
    """An interface for components that can be animated to produce an AnimationClip."""

    def set_animation_frame(self, frame: T) -> None:
        """Set or update the component based on the frame."""
        msg = "The 'set_frame' method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_animation_frame(self) -> T:
        """Get the animation frame based on the component data."""
        msg = "The 'get_frame' method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def create_animation(self, fps: int) -> AnimationBuilder[T]:
        """Return an AnimationBuilder to build out the animation."""
        return AnimationBuilder(fps)
