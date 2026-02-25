"""A component that keeps track of time between frames."""

import time


class Singleton(type):
    """An implementation of the Singleton pattern as a 'type' / 'metaclass'."""

    _instances = {}  # noqa: RUF012

    def __call__(cls, *args, **kwargs):  # noqa: ANN002, ANN003, ANN204, D102
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)  # noqa: UP008
        return cls._instances[cls]


class DeltaTime(metaclass=Singleton):
    """A component that keeps track of time between frames."""

    def __init__(self) -> None:
        """Initialize the DeltaTime."""
        self.last_frame_time: float | None = None

    def update_delta(self) -> None:
        """Set current frame."""
        self.last_frame_time = time.time()

    @property
    def delta_time(self) -> float:
        """Get the delta time."""
        return time.time() - self.last_frame_time  # pyright: ignore[reportOperatorIssue]
