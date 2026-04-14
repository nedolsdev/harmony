"""Input example scene."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from core.packages.input.action_map import ActionMap
from core.packages.input.bindings.key_binding import KeyBinding
from core.packages.input.bindings.mouse_binding import MouseMoveBinding
from core.packages.input.interactions.default import DefaultInteraction
from core.packages.input.interactions.press import PressInteraction
from example_scenes.camera_util import create_camera_game_object
from game.scene import Scene

if TYPE_CHECKING:
    from core.packages.input.input_action import InputAction
    from core.packages.input.input_system import InputSystem
    from game.sorting_layer import SortingLayerManager


def create_gameplay_action_map() -> ActionMap:
    """Create a test input system."""
    gameplay = ActionMap()

    jump: InputAction[float] = gameplay.add_action("jump")
    move: InputAction[tuple[float, float]] = gameplay.add_action("move")

    gameplay.add_binding(KeyBinding(pygame.K_SPACE, jump, DefaultInteraction()))
    gameplay.add_binding(KeyBinding(pygame.K_w, jump, PressInteraction()))

    gameplay.add_binding(MouseMoveBinding(move))

    jump.on_performed(lambda action: print("jump performed"))  # noqa: ARG005, T201
    move.on_performed(lambda action: print(f"move: {action.value}"))  # noqa: T201

    return gameplay


def create_input_scene(window_size: int, layers: SortingLayerManager, input_system: InputSystem) -> Scene:
    """Return a Scene configured for testing input behavior."""
    scene = Scene()

    input_system.create_map("gameplay", action_map=create_gameplay_action_map())

    default_layer = layers.get_layer("Default")

    scene.add_game_object(create_camera_game_object(window_size, default_layer))

    return scene
