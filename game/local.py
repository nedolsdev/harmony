"""An interface to support a local version of a component."""

from typing import Generic, TypeVar

T = TypeVar("T", bound="Local")


class Local(Generic[T]):
    """An interface to support a local version of a component."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Get local value."""
        super().__init__(*args, **kwargs)
        self.local: T

    def awake_local(self) -> None:
        """Awake the local version of the component."""
        msg = "Should be implemented in subclasses."
        raise NotImplementedError(msg)

    def has_local(self) -> bool:
        """Check if local exists on Component."""
        return hasattr(self, "local")
