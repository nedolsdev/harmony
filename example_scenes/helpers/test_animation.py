"""A test animation."""

from __future__ import annotations

import math

from core.components.transform import Transform
from core.packages.animation.animator import Animator
from core.packages.animation.clip import NO_ANIMATION, KeyFrame, KeyFrameBlender, KeyFramedAnimationClip
from core.packages.animation.controller import (
    ENTRY_STATE,
    AnimationController,
    AnimationLayer,
    AnimationState,
    AnimationTransition,
)
from core.packages.animation.frame import ScalarFrame, Vector2Frame
from core.packages.geometry.vector2 import Vector2


class BasicVector2LERP(KeyFrameBlender[Vector2Frame]):
    """Test blender for basic LERP between two Vector2s."""

    def blend(
        self,
        frame_number: int,
        current_frame: KeyFrame[Vector2Frame],
        next_key_frame: KeyFrame[Vector2Frame],
    ) -> Vector2Frame:
        """Produce an AnimationFrame between the current and next frame."""
        # basic LERP
        percentage = self.get_percentage_of_transition(frame_number, current_frame, next_key_frame)
        v1 = current_frame.frame.vector
        v2 = next_key_frame.frame.vector
        v3 = v1 + (v2 - v1) * percentage
        return Vector2Frame(v3)


class BasicScalarLERP(KeyFrameBlender[ScalarFrame]):
    """Test blender for basic LERP between two scalar values."""

    def blend(
        self,
        frame_number: int,
        current_frame: KeyFrame[ScalarFrame],
        next_key_frame: KeyFrame[ScalarFrame],
    ) -> ScalarFrame:
        """Produce an AnimationFrame between the current and next frame."""
        # basic LERP
        percentage = self.get_percentage_of_transition(frame_number, current_frame, next_key_frame)
        v1 = current_frame.frame.value
        v2 = next_key_frame.frame.value
        v3 = v1 + (v2 - v1) * percentage
        return ScalarFrame(v3)


def create_test_rotation_animator() -> Animator:
    """Create a test animator component for a rotating animation in the example scene."""
    blender = BasicScalarLERP()

    clip = KeyFramedAnimationClip(fps=60, blender=blender, target=Transform.get_fields().local_rotation, loop=False)

    clip.add_key_frame(
        KeyFrame(
            ScalarFrame(0),
            0,
        ),
    )
    clip.add_key_frame(
        KeyFrame(
            ScalarFrame(math.pi // 2),
            5,
        ),
    )
    clip.add_key_frame(
        KeyFrame(
            ScalarFrame(0),
            10,
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

    return Animator(controller=test_controller)


def create_test_animator() -> Animator:
    """Create a test animator component for the example scene."""
    blender = BasicVector2LERP()

    clip = KeyFramedAnimationClip(fps=60, blender=blender, target=Transform.get_fields().local_position)

    clip.add_key_frame(
        KeyFrame(
            Vector2Frame(Vector2(0, 0)),
            0,
        ),
    )
    clip.add_key_frame(
        KeyFrame(
            Vector2Frame(Vector2(25, 25)),
            30,
        ),
    )
    clip.add_key_frame(
        KeyFrame(
            Vector2Frame(Vector2(0, 0)),
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

    return Animator(controller=test_controller)
