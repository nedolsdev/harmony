"""The animator component that acts on the the animation controller."""

from __future__ import annotations

from typing import TYPE_CHECKING

from game.behavior import Behavior

if TYPE_CHECKING:
    from core.packages.animation.controller import AnimationController
    from game.event_handler import EventHandler


# parameter types are Trigger, Int, Float, Bool


class Animator[DataT](Behavior):
    """The animator component that acts on the animation controller."""

    def __init__(self, controller: AnimationController[DataT]) -> None:
        """Initialize the Animation Component with the AnimationController."""
        super().__init__()
        self.controller: AnimationController[DataT] = controller

    def awake(self) -> None:
        """Event call when the script instance is created."""

    def start(self) -> None:
        """Event call on the first frame of the game."""

    def update(self) -> None:
        """Update the component every frame."""
        self.controller.update(self.game_object)

    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    def copy(self) -> Animator:
        """Create a copy of the game component."""
        # NOTE: This doesn't make a deep copy of the AnimationController which could cause issues?
        return Animator(self.controller)
