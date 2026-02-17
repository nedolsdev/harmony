"""A test animation."""

from core.components.position import Position, PositionFrame
from core.packages.animation.clip import NO_ANIMATION, KeyFrame, KeyFrameBlender, KeyFramedAnimationClip
from core.packages.animation.controller import (
    ENTRY_STATE,
    AnimationController,
    AnimationLayer,
    AnimationState,
    AnimationTransition,
)
from core.packages.animation.frame import VectorFrame


class BasicPositionLERP(KeyFrameBlender[PositionFrame]):
    """Test blender for basic LERP between two positions."""

    def blend(
        self,
        frame_number: int,
        current_frame: KeyFrame[PositionFrame],
        next_key_frame: KeyFrame[PositionFrame],
    ) -> PositionFrame:
        """Produce an AnimationFrame between the current and next frame."""
        # basic LERP
        percentage = self.get_percentage_of_transition(frame_number, current_frame, next_key_frame)

        v1 = current_frame.frame.vector
        v2 = next_key_frame.frame.vector

        v3 = (
            int(v1[0] + percentage * (v2[0] - v1[0])),
            int(v1[1] + percentage * (v2[1] - v1[1])),
            int(v1[2] + percentage * (v2[2] - v1[2])),
        )

        return PositionFrame(v3)


blender = BasicPositionLERP()

clip = KeyFramedAnimationClip(fps=60, blender=blender, target=Position)

clip.add_key_frame(
    KeyFrame(
        VectorFrame((50, 50, 50)),
        0,
    ),
)
clip.add_key_frame(
    KeyFrame(
        VectorFrame((75, 75, 75)),
        30,
    ),
)
clip.add_key_frame(
    KeyFrame(
        VectorFrame((50, 50, 50)),
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
