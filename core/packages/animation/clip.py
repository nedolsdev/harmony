"""An AnimationClip defines the sequence of AnimationFrames played by the animation."""

from core.packages.animation.frame import AnimationFrame


class AnimationClip:
    """An AnimationClip defines the sequence of AnimationFrames played by the animation at a given fps."""

    def __init__(self, fps: int) -> None:
        """Initialize the AnimationClip with an FPS."""
        self.current_frame: int = 0
        self.fps = fps

    def get_next_animation_frame(self, *, loop: bool = False) -> AnimationFrame | None:
        """Get the next animation frame if it exists. Returns 'None' when at the end."""
        if self.animation_complete():
            if not loop:
                return None
            # go back to the starting frame
            self.current_frame = -1

        self.current_frame += 1
        return self.get_frame(self.current_frame)

    def reset(self) -> None:
        """Reset the animation back to the beginning frame."""
        self.current_frame = 0

    def animation_complete(self) -> bool:
        """Check whether the animation is on the last frame."""
        return self.current_frame == self.get_number_of_frames() - 1

    def get_animation_time(self) -> float:
        """Get the animation time in seconds."""
        return self.get_number_of_frames() / self.fps

    def get_number_of_frames(self) -> int:
        """Get the number of frames the clip contains."""
        msg = "The 'get_number_of_frames' method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_frame(self, frame: int) -> AnimationFrame:
        """Get the AnimationFrame for a given frame number."""
        msg = "The 'get_frame' method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_fps(self) -> int:
        """Get the number of AnimationFrames played every second."""
        return self.fps


class SimpleAnimationClip(AnimationClip):
    """A SimpleAnimationClip has a list of static AnimationFrame that are played in sequence."""

    def __init__(self, fps: int) -> None:
        """Initialize the SimpleAnimationClip with an empty list of AnimationFrames."""
        super().__init__(fps)
        self.frames: list[AnimationFrame] = []

    def get_number_of_frames(self) -> int:
        """Get the number of frames the clip contains."""
        return len(self.frames)

    def get_frame(self, frame: int) -> AnimationFrame:
        """Get the AnimationFrame for a given frame number."""
        return self.frames[frame]

    def add_frame(self, animation_frame: AnimationFrame) -> None:
        """Add an AnimationFrame to the AnimationClip."""
        self.frames.append(animation_frame)


NO_ANIMATION = AnimationClip(fps=0)
