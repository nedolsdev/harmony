"""Play sound on start test component."""

from __future__ import annotations

from typing import override

from harmony.core.components.transform import Transform
from harmony.core.packages.audio.audio_source import AudioSource
from harmony.core.packages.geometry.vector2 import Vector2
from harmony.core.packages.timing.delta_time import DeltaTime
from harmony.game.behavior import Behavior


class PlaySoundTest(Behavior):
    """Play sound on start test component."""

    transform: Transform

    def __init__(self) -> None:
        """Initialize the PlaySound test component."""
        super().__init__()

        # move back and forth between two points
        self.point1 = Vector2(100, 0)
        self.point2 = Vector2(-100, 0)

        # speed in px per second
        self.speed = 50

        # start moving right
        self.t = 0
        self.move_direction = 1

    @override
    def awake(self) -> None:
        """Event call when the script instance is created."""
        self.transform = self.game_object.get_component(Transform)

    @override
    def start(self) -> None:
        """Initialize the sprite component."""
        source = self.game_object.get_component(AudioSource)
        source.play()

    @override
    def update(self) -> None:
        """Update the sprite component."""
        dt = DeltaTime.get_delta_time()

        total_distance = (self.point2 - self.point1).magnitude()
        dt_t = (self.speed * dt) / total_distance

        self.t += dt_t * self.move_direction

        if self.t >= 1.0:
            self.t = 1.0
            self.move_direction = -1
        elif self.t <= 0.0:
            self.t = 0.0
            self.move_direction = 1

        self.transform.local_position = self.point1 + (self.point2 - self.point1) * self.t
