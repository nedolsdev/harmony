"""Basic Canvas component for the UI package."""

from enum import Enum, auto

from core.packages.ui.components.ui_element import UIElement


class CanvasRenderModes(Enum):
    """How the canvas is rendered (part of the world or on top of it separately)."""

    WORLD_SPACE = auto()
    SCREEN_SPACE_OVERLAY = auto()


class Canvas(UIElement):
    """Basic Canvas component for the UI package."""

    def __init__(
        self,
    ) -> None:
        """Initialize the Canvas component."""
        super().__init__()
