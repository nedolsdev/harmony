"""An AnimationClip defines the sequence of AnimationFrames played by the animation."""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, override

from core.packages.animation.frame import AnimationFrame

if TYPE_CHECKING:
    from game.component import GameComponent

T = TypeVar("T", bound=AnimationFrame)


class AnimationClip[T: AnimationFrame]:
    """An AnimationClip defines the sequence of AnimationFrames played by the animation at a given fps."""

    def __init__(
        self,
        fps: int,
        target: type[GameComponent] | None,
        *,
        loop: bool = False,
    ) -> None:
        """Initialize the AnimationClip with an FPS."""
        self.current_frame: int = 0
        self.fps = fps
        self.target = target
        self.loop = loop

    def get_next_animation_frame(self) -> T | None:
        """Get the next animation frame if it exists. Returns 'None' when at the end."""
        if self.animation_complete():
            if not self.loop:
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

    def get_frame(self, frame: int) -> T:
        """Get the AnimationFrame for a given frame number."""
        msg = "The 'get_frame' method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_fps(self) -> int:
        """Get the number of AnimationFrames played every second."""
        return self.fps


class KeyFrame[T: AnimationFrame]:
    """A KeyFrame defines an AnimationFrame played at a particular frame number within an AnimationClip."""

    def __init__(self, frame: T, frame_number: int) -> None:
        """Initialize the KeyFrame with a given AnimationFrame and frame number."""
        super().__init__()
        self.frame = frame
        self.frame_number = frame_number


class KeyFrameBlender[T: AnimationFrame]:
    """A KeyFrame Blender defines how to fill the AnimationFrames between two KeyFrames."""

    def blend(self, frame_number: int, current_frame: KeyFrame[T], next_key_frame: KeyFrame[T]) -> T:
        """Produce an AnimationFrame between the current and next frame."""
        msg = "This method should be implemented in subclasses."
        raise NotImplementedError(msg)

    def get_frame_count_between_key_frames(self, current_frame: KeyFrame, next_key_frame: KeyFrame) -> int:
        """Get the number of frames between each frame. (e.g. start=50, end=60 => count=10)."""
        return next_key_frame.frame_number - current_frame.frame_number

    def get_current_step_of_frame(self, frame_number: int, current_frame: KeyFrame) -> int:
        """Get the current frame step between frames. (e.g. frame=53, start=50, end=60 => step=3)."""
        return frame_number - current_frame.frame_number

    def get_percentage_of_transition(
        self,
        frame_number: int,
        current_frame: KeyFrame,
        next_key_frame: KeyFrame,
    ) -> float:
        """Get the percentage of how far the current frame is along the transition between KeyFrames."""
        count = self.get_frame_count_between_key_frames(current_frame, next_key_frame)
        step = self.get_current_step_of_frame(frame_number, current_frame)
        return step / count


class KeyFramedAnimationClip(AnimationClip[T]):
    """A KeyFramedAnimationClip defines KeyFrames that are transitioned between in sequence."""

    def __init__(
        self,
        fps: int,
        blender: KeyFrameBlender[T],
        target: type[GameComponent],
        *,
        loop: bool = True,
    ) -> None:
        """Initialize the KeyFramedAnimationClip with an FPS and a KeyFrameMixer."""
        super().__init__(fps, target, loop=loop)
        self.key_frames: list[KeyFrame[T]] = []
        self.blender = blender

    @override
    def get_number_of_frames(self) -> int:
        """Get the number of frames the clip contains."""
        last_frame = self.key_frames[-1]
        # the last key frame is always the last frame of the animation
        return last_frame.frame_number

    def get_current_key_frame_index(self, frame_number: int) -> int:
        """Get the index of the current key frame."""
        for i, key_frame in enumerate(self.key_frames):
            if key_frame.frame_number > frame_number:
                return i - 1
        return len(self.key_frames) - 1

    def get_key_frame(self, index: int) -> KeyFrame[T]:
        """Get the KeyFrame at a given index."""
        return self.key_frames[index]

    def get_frame(self, frame: int) -> T:
        """Get the AnimationFrame for a given frame number."""
        current_key_frame_index = self.get_current_key_frame_index(frame)
        current_key_frame = self.get_key_frame(current_key_frame_index)

        # if it is the last frame then we can't mix it because there is no next frame
        if frame == self.get_number_of_frames():
            return current_key_frame.frame

        # otherwise we just grab the next frame
        next_key_frame = self.get_key_frame(current_key_frame_index + 1)

        # and then use the mixer to produce the next intermediate frame
        return self.blender.blend(frame, current_key_frame, next_key_frame)

    def add_key_frame(self, key_frame: KeyFrame[T]) -> None:
        """Add an AnimationFrame to the AnimationClip."""
        self.key_frames.append(key_frame)

        # ensure that key frames are always in order
        self.key_frames.sort(key=lambda key_frame: key_frame.frame_number)


class EmptyAnimationClip(AnimationClip):
    """Empty AnimationClip."""

    @override
    def get_number_of_frames(self) -> int:
        """Get the number of frames the clip contains."""
        return 0

    @override
    def get_frame(self, frame: int) -> AnimationFrame:
        """Get the AnimationFrame for a given frame number."""
        return AnimationFrame()


NO_ANIMATION = EmptyAnimationClip(fps=0, target=None)
