"""A test animation."""

from core.components.transform import Transform
from core.packages.animation.clip import NO_ANIMATION, KeyFrame, KeyFrameBlender, KeyFramedAnimationClip
from core.packages.animation.controller import (
    ENTRY_STATE,
    AnimationController,
    AnimationLayer,
    AnimationState,
    AnimationTransition,
)
from core.packages.animation.frame import VectorFrame
from game.vector2 import Vector2


class BasicPositionLERP(KeyFrameBlender[VectorFrame]):
    """Test blender for basic LERP between two positions."""

    def blend(
        self,
        frame_number: int,
        current_frame: KeyFrame[VectorFrame],
        next_key_frame: KeyFrame[VectorFrame],
    ) -> VectorFrame:
        """Produce an AnimationFrame between the current and next frame."""
        # basic LERP
        percentage = self.get_percentage_of_transition(frame_number, current_frame, next_key_frame)
        v1 = current_frame.frame.vector
        v2 = next_key_frame.frame.vector
        v3 = v1 + (v2 - v1) * percentage
        return VectorFrame(v3)


blender = BasicPositionLERP()

clip = KeyFramedAnimationClip(fps=60, blender=blender, target=Transform)

clip.add_key_frame(
    KeyFrame(
        VectorFrame(Vector2(0, 0)),
        0,
    ),
)
clip.add_key_frame(
    KeyFrame(
        VectorFrame(Vector2(25, 25)),
        30,
    ),
)
clip.add_key_frame(
    KeyFrame(
        VectorFrame(Vector2(0, 0)),
        60,
    ),
)


idle = AnimationState("Idle", NO_ANIMATION)
move = AnimationState("Move", clip)


class NoData:
    """No data needed for this Animation."""


test_controller = AnimationController(NoData(), init_default_layer=False)

default_layer = AnimationLayer("Default")

transition = AnimationTransition()

# instantly enters the move animation to play it
default_layer.add_edge(ENTRY_STATE, move, transition)

default_layer.add_edge(idle, move, transition)

test_controller.add_layer(default_layer)
