"""A component that fires an event after a period of time."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from core.packages.timing.delta_time import DeltaTime
from game.behavior import Behavior
from game.component import GameComponent

if TYPE_CHECKING:
    from collections.abc import Callable

    from game.event_handler import EventHandler


class Timer(GameComponent):
    """A component that fires an event after a period of time."""

    # TODO: Add grid gap  # noqa: TD003

    def __init__(self, duration: float, callback: Callable[[], None]) -> None:
        """Initialize the Grid component with a duration in seconds."""
        super().__init__()
        self.duration = duration
        self.time_left: float | None = None
        self.callback = callback
        self.paused = False

    @property
    def running(self) -> bool:
        """Check if the timer is running."""
        return self.time_left is not None

    def start_timer(self) -> None:
        """Start a timer for a given duration."""
        self.time_left = self.duration

    def reset_timer(self) -> None:
        """Reset the timer."""
        self.time_left = None

    def pause(self) -> None:
        """Pause the timer."""
        self.paused = True

    def unpause(self) -> None:
        """Unpause the timer."""
        self.paused = False

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""

    @override
    def start(self) -> None:
        """Initialize the sprite component."""

    @override
    def update(self) -> None:
        """Update the sprite component."""
        if not self.running or self.paused:
            return

        assert self.time_left is not None  # noqa: S101 (just for type hint, 100% always passes)

        # update time left
        self.time_left -= DeltaTime().delta_time

        if self.running and self.time_left <= 0:
            self.callback()
            self.reset_timer()

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def copy(self) -> Timer:
        """Create a copy of the timer component."""
        return self


# example of use


class ComponentUsingTimer(Behavior):
    """A component that uses a timer."""

    timer: Timer

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        timer = Timer(5, lambda: print("Hello world!"))
        self.game_object.add_component(timer)
        self.timer = timer

    @override
    def start(self) -> None:
        """Initialize the sprite component."""
        self.timer.start_timer()

    @override
    def update(self) -> None:
        """Update the sprite component."""

    @override
    def add_events(self, event_handler: EventHandler) -> None:
        """Add events to the event handler for this component."""

    @override
    def copy(self) -> ComponentUsingTimer:
        """Create a copy of the timer component."""
        return self
