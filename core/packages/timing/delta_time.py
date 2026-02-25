"""A component that keeps track of time between frames."""


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
        self._dt: float = 0.0

    def set(self, dt: float) -> None:
        """Set the delta time."""
        self._dt = dt

    @property
    def delta_time(self) -> float:
        """Get the delta time."""
        return self._dt

    @staticmethod
    def get_delta_time() -> float:
        """Get the delta time."""
        return DeltaTime().delta_time
