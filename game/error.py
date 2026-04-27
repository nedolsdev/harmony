"""Some base errors that are useful for many different parts of the engine."""

from __future__ import annotations

from types import MethodType
from typing import Any


def get_class_that_defined_method(method: MethodType) -> type[Any]:
    """Get the class that defined a bound method."""
    if not isinstance(method, MethodType):
        msg = "Incorrect use 'not_implemented' or 'get_class_that_defined_method'. Expected a bound method."
        raise TypeError(msg)
    return type(method.__self__)


def not_implemented(method: MethodType) -> None:
    """Raise a not implemented error for a given class."""
    cls = get_class_that_defined_method(method)
    msg = f"'{cls.__name__}' does not implement the required abstract method '{method.__name__}'."
    raise NotImplementedError(msg)


class InvalidArgumentCombinationError(RuntimeError):
    """Exception raised when an illegal combination of arguments is used."""


class MissingComponentDependencyError(RuntimeError):
    """Exception raised when an operation is missing a component dependency for it to work."""


class DataAlreadyExistsError(RuntimeError):
    """Exception raised when data that already exists is tried to be set or added."""
