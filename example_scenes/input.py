"""Input example scene."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from example_scenes.helpers.camera_util import create_camera_game_object
from harmony.core.packages.input.action_map import ActionMap
from harmony.core.packages.input.bindings.key_binding import KeyBinding
from harmony.core.packages.input.bindings.mouse_binding import MouseMoveBinding
from harmony.core.packages.input.composite_binding import CompositeBinding
from harmony.core.packages.input.interactions.tap import TapInteraction
from harmony.game.scene import Scene

if TYPE_CHECKING:
    from harmony.core.packages.input.input_action import InputAction
    from harmony.core.packages.input.input_binding import InputBinding
    from harmony.core.packages.input.input_system import InputSystem
    from harmony.game.sorting_layer import SortingLayerManager
    from harmony.game.window import WindowSettings


def create_gameplay_action_map() -> ActionMap:
    """Create a test input system."""
    gameplay = ActionMap()

    jump: InputAction[float] = gameplay.add_action("jump", 0)
    move: InputAction[tuple[float, float]] = gameplay.add_action("move", (0, 0))

    gameplay.add_binding(KeyBinding(pygame.K_SPACE, jump, TapInteraction()))
    gameplay.add_binding(MouseMoveBinding(move))

    def wasd_compose(values: dict[str, float]) -> tuple[float, float]:
        """Combine WASD inputs into a 2D vector."""
        x = values.get("right", 0.0) - values.get("left", 0.0)
        y = values.get("down", 0.0) - values.get("up", 0.0)
        return (x, y)

    wasd_parts: dict[str, InputBinding[float]] = {
        "up": KeyBinding(pygame.K_w, move.as_composite_part()),
        "down": KeyBinding(pygame.K_s, move.as_composite_part()),
        "left": KeyBinding(pygame.K_a, move.as_composite_part()),
        "right": KeyBinding(pygame.K_d, move.as_composite_part()),
    }

    gameplay.add_binding(
        CompositeBinding(
            action=move,
            parts=wasd_parts,
            compose=wasd_compose,
        ),
    )

    jump.on_performed(lambda action: print("jump performed"))  # noqa: ARG005, T201
    move.on_performed(lambda action: print(f"move: {action.value}"))  # noqa: T201

    return gameplay


def create_input_scene(
    window_settings: WindowSettings,
    layers: SortingLayerManager,
    input_system: InputSystem,
) -> Scene:
    """Return a Scene configured for testing input behavior."""
    scene = Scene()

    input_system.create_map("gameplay", action_map=create_gameplay_action_map())

    default_layer = layers.get_layer("Default")

    scene.add_game_object(create_camera_game_object(window_settings, default_layer))

    return scene
