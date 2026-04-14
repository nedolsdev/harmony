"""The logging module provides a logger for the game engine."""

from __future__ import annotations

import logging
import sys
from typing import ClassVar


class EngineLogger:
    """Central logging manager for the engine."""

    _configured: ClassVar[bool] = False
    _loggers: ClassVar[dict[str, logging.Logger]] = {}

    @classmethod
    def setup(
        cls,
        level: int = logging.DEBUG,
        stream: logging.StreamHandler | None = None,
        log_file: str | None = None,
    ) -> None:
        """Configure global logging output and format."""
        if cls._configured:
            return

        if stream is None:
            stream = logging.StreamHandler(sys.stdout)

        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        formatter = logging.Formatter("[%(asctime)s] [%(name)s] %(message)s", "%H:%M:%S")

        # console handler
        console_handler = stream
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Optional file handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        cls._configured = True
        cls.get_logger("Engine").info("Logging setup complete.")

    @classmethod
    def get_logger(cls, name: str, level: int | None = None) -> logging.Logger:
        """Return a configured logger with the given name."""
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        if level is not None:
            logger.setLevel(level)

        cls._loggers[name] = logger
        return logger
