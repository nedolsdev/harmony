"""Main entry point for the Agent World game."""

from agent_world.components.movement import Movement
from agent_world.objects.agent import Agent
from core.components.grid_render import GridRender
from core.components.position import Position
from core.components.render_layer import RenderLayer
from core.components.sprite_2d import Sprite2D, SpriteImage
from core.objects.grid import GridGenerator
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.material import GrayscaleMaterial
from game.object_builder import GameObjectBuilder
from game.render_pipeline import RenderPipeline
from game.runner import Runner
from game.scene import Scene
from game.scene_manager import SceneManager


def main() -> None:
    """Initialize the game and start the renderer."""
    scene_manager = SceneManager()

    scene = Scene("Main Scene")

    scene_manager.add_scene(scene)
    scene_manager.set_active_scene("Main Scene")

    event_handler = EventHandler()

    grid_size = 10
    tile_size = 60
    window_size = grid_size * tile_size

    renderer = RenderPipeline(title="Agent World", window_width=window_size, window_height=window_size)
    renderer.sorting_layers.create_layer("Background", 0)
    renderer.sorting_layers.create_layer("Default", 10)
    renderer.sorting_layers.create_layer("UI", 100)

    bg_layer = renderer.sorting_layers.get_layer("Background")
    default_layer = renderer.sorting_layers.get_layer("Default")

    game = Runner(renderer, event_handler, scene)

    grid = GridGenerator.generate(grid_size=grid_size, tile_size=tile_size)
    scene.add_game_object(grid)
    grid.add_component(GridRender(grid))
    grid.add_component(RenderLayer(bg_layer))

    prefab = (
        GameObjectBuilder(Agent)
        .add_component(Movement(grid))  # custom component
        .add_component(Position(0, 0))
        .add_component(
            Sprite2D(
                width=tile_size,
                height=tile_size,
                material=GrayscaleMaterial(),
                image=SpriteImage("assets/sprites/agent.png"),
            ),
        )
        .add_component(RenderLayer(default_layer))
        .add_tag("agent")
        .build_as_prefab()
    )

    agent2 = prefab.create_object()
    agent3 = prefab.create_object()

    # set x and y position for the second agent
    agent2.get_component(Position).set_coordinates(tile_size, tile_size)

    scene.add_game_object(agent2)
    scene.add_game_object(agent3)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
