"""The image cache module contains the ImageCache class for managing image loading and caching."""
from __future__ import annotations

import logging
import os
from collections import OrderedDict
from typing import ClassVar

import pygame


class ImageCache:
    """An image cache with LRU eviction and fallback support."""

    _cache: ClassVar[OrderedDict[str, pygame.Surface]] = OrderedDict()
    _fallback: ClassVar[pygame.Surface | None] = None
    _max_size: ClassVar[int | None] = None  # unlimited
    _logger: ClassVar[logging.Logger] = logging.getLogger("ImageCache")

    @classmethod
    def set_max_size(cls, max_size: int | None) -> None:
        """Set a maximum number of images to cache. None = unlimited."""
        cls._max_size = max_size
        cls._evict_if_needed()

    @classmethod
    def _evict_if_needed(cls) -> None:
        """Evict least recently used images if cache is over limit."""
        if cls._max_size is None:
            return
        while len(cls._cache) > cls._max_size:
            evicted, _ = cls._cache.popitem(last=False)
            cls._logger.debug("Evicting: %s", evicted)

    @classmethod
    def _convert(cls, surface: pygame.Surface) -> pygame.Surface:
        """Convert the surface to a format suitable for rendering."""
        return surface.convert_alpha() if surface.get_alpha() else surface.convert()

    @classmethod
    def load(cls, path: str) -> pygame.Surface:
        """Load an image from the given path, caching it for future use."""
        norm_path = os.path.normpath(path)

        if norm_path in cls._cache:
            cls._cache.move_to_end(norm_path)
        else:
            try:
                raw = pygame.image.load(norm_path)
                surface = cls._convert(raw)
                cls._cache[norm_path] = surface
                cls._logger.debug("Loaded: %s", norm_path)
                cls._evict_if_needed()
            except Exception as _:
                cls._logger.exception("Failed to load image '%s'", norm_path)
                return cls.get_fallback_copy()

        return cls._cache[norm_path]

    @classmethod
    def get_fallback(cls) -> pygame.Surface:
        """Get a fallback image if no image is loaded."""
        if cls._fallback is None:
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            surface.fill((255, 255, 255, 255))
            cls._fallback = cls._convert(surface)
            cls._logger.debug("Created fallback image")
        return cls._fallback

    @classmethod
    def get_fallback_copy(cls) -> pygame.Surface:
        """Get a copy of the fallback image."""
        return cls.get_fallback().copy()

    @classmethod
    def preload(cls, paths: list[str]) -> None:
        """Preload a list of images into the cache."""
        for path in paths:
            cls.load(path)

    @classmethod
    def unload(cls, path: str) -> None:
        """Unload an image from the cache."""
        norm_path = os.path.normpath(path)
        if norm_path in cls._cache:
            del cls._cache[norm_path]
            cls._logger.debug("Unloaded: %s", norm_path)

    @classmethod
    def clear(cls) -> None:
        """Clear the image cache."""
        cls._cache.clear()
        cls._fallback = None
        cls._logger.debug("Cache cleared")
