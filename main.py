"""Main entry point for the Agent World game."""

from rich.traceback import install

from agent_world.animations.test_animation import test_controller
from agent_world.objects.agent import Agent
from agent_world.objects.test_tile_map import grid, tile_map, tile_map_renderer
from core.assets.sprite_image import SpriteImage
from core.components.line_2d import Line2D
from core.components.position import Position
from core.components.render_layer import RenderLayer
from core.components.rotation import Rotation
from core.components.sprite_2d import Sprite2D
from core.objects.empty import Empty
from core.packages.animation.animator import Animator
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.material import ColorMaterial, GrayscaleMaterial
from game.object_builder import GameObjectBuilder
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene import Scene
from game.scene_manager import SceneManager

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    scene_manager = SceneManager()

    scene = Scene("Main Scene")

    scene_manager.add_scene(scene)
    scene_manager.set_active_scene("Main Scene")

    event_handler = EventHandler()

    grid_size = 12
    tile_size = 60
    window_size = grid_size * tile_size

    renderer = RenderPipeline(title="Agent World", window_width=window_size, window_height=window_size)
    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    bg_layer = renderer.sorting_layers.get_layer("Background")
    default_layer = renderer.sorting_layers.get_layer("Default")

    game = Runner(renderer, event_handler, scene)

    prefab = (
        GameObjectBuilder(Agent)
        .add_component(Position(0 + tile_size * 10 // 2, 0 + tile_size * 10 // 2))
        .add_component(
            Sprite2D(
                width=tile_size,
                height=tile_size,
                material=GrayscaleMaterial(),
                image=SpriteImage("assets/sprites/agent.png"),
            ),
        )
        .add_component(Rotation(degrees=0))
        .add_component(RenderLayer(default_layer))
        .add_tag("agent")
        .build_as_prefab()
    )

    grid_obj = (
        GameObjectBuilder(Empty)
        .add_component(Position(x=50, y=50))
        .add_component(RenderLayer(bg_layer))
        .add_component(grid)
        .add_component(tile_map)
        .add_component(tile_map_renderer)
        .build_as_prefab()
    )

    scene.add_game_object(grid_obj.create_object())

    agent2 = prefab.create_object()

    scene.add_game_object(agent2)

    # line
    line_prefab = (
        GameObjectBuilder(Agent)
        .add_component(Position(250, 250))
        .add_component(
            Line2D(
                start=Position(0, 0),
                end=Position(100, 100),
                material=ColorMaterial((0, 255, 0)),
                width=5,
            ),
        )
        .add_component(
            Line2D(
                start=Position(0, 0),
                end=Position(-100, 100),
                material=ColorMaterial((255, 0, 0)),
                width=5,
            ),
        )
        .add_component(Animator(test_controller))
        .add_component(RenderLayer(default_layer))
        .build_as_prefab()
    )

    line_object = line_prefab.create_object()
    scene.add_game_object(line_object)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
