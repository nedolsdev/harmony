"""Some base errors that are useful for many different parts of the engine."""


class InvalidArgumentCombinationError(RuntimeError):
    """Exception raised when an illegal combination of arguments is used."""


class MissingComponentDependencyError(RuntimeError):
    """Exception raised when an operation is missing a component dependency for it to work."""


class DataAlreadyExistsError(RuntimeError):
    """Exception raised when data that already exists is tried to be set or added."""
