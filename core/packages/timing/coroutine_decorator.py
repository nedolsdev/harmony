"""Coroutine decorator."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec

from core.packages.timing.coroutine import Coroutine, CoroutineGenerator

P = ParamSpec("P")

type CoroutineFactory[**P] = Callable[P, Coroutine]


def coroutine[**P](func: Callable[P, CoroutineGenerator]) -> CoroutineFactory[P]:
    """Wrap a generator function into a Coroutine."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Coroutine:
        return Coroutine(func(*args, **kwargs))

    return wrapper
