"""Basic Canvas component for the UI package."""

from enum import Enum, auto

from core.packages.ui.components.ui_element import UIElement


class CanvasRenderMode(Enum):
    """How the canvas is rendered (part of the world or on top of it separately)."""

    WORLD_SPACE = auto()
    SCREEN_SPACE_OVERLAY = auto()


class Canvas(UIElement):
    """Basic Canvas component for the UI package."""

    def __init__(self, *, mode: CanvasRenderMode = CanvasRenderMode.SCREEN_SPACE_OVERLAY) -> None:
        """Initialize the Canvas component."""
        super().__init__()
        self.mode = mode
