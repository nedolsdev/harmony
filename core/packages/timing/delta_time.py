"""A component that keeps track of time between frames."""

from __future__ import annotations


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
        self._unscaled_dt: float = 0.0
        self._time_scale: float = 1

    def set(self, dt: float) -> None:
        """Set the delta time."""
        self._unscaled_dt = dt

    def set_time_scale(self, scale: float) -> None:
        """Set the time scale."""
        if scale <= 0:
            msg = "Cannot set a negative time scale. Time scale must be greater than or equal to 0."
            raise ValueError(msg)
        self._time_scale = scale

    @property
    def delta_time(self) -> float:
        """Get the delta time."""
        return self._unscaled_dt * self._time_scale

    @property
    def unscaled_delta_time(self) -> float:
        """Get the real delta time (ignores time scale)."""
        return self._unscaled_dt

    @staticmethod
    def get_delta_time() -> float:
        """Get the delta time."""
        return DeltaTime().delta_time

    @staticmethod
    def get_unscaled_delta_time() -> float:
        """Get the real delta time (ignores time scale)."""
        return DeltaTime().unscaled_delta_time
