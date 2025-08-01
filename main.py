"""Main entry point for the Agent World game."""

from agent_world.components.movement import Movement
from agent_world.objects.agent import Agent
from core.components.grid_render import GridRender
from core.components.position import Position
from core.components.sprite_2d import SpriteImage
from core.objects.grid import GridGenerator
from game.component_factory import ComponentFactory
from game.draw import Renderer
from game.event_handler import EventHandler
from game.image_cache import ImageCache
from game.logging import EngineLogger
from game.material import ColorMaterial
from game.object_builder import GameObjectBuilder
from game.runner import Runner
from game.state import GameState


def main() -> None:
    """Initialize the game and start the renderer."""
    state = GameState()
    event_handler = EventHandler()

    grid_size = 10
    tile_size = 60
    window_size = grid_size * tile_size

    grid = GridGenerator.generate(grid_size=grid_size, tile_size=tile_size)
    state.add_game_object(grid)
    grid.add_component(GridRender(grid))

    prefab = (
        GameObjectBuilder(Agent)
        .add_component(Movement(grid))  # custom component
        .add_component(ComponentFactory.position(0, 0))
        .add_component(
            ComponentFactory.sprite_2d(
                width=tile_size,
                height=tile_size,
                material=ColorMaterial((50, 150, 250), 128),
                image=SpriteImage("assets/sprites/agent.png"),
            ),
        )
        .add_tag("agent")
        .build_as_prefab()
    )

    agent2 = prefab.create_object()
    agent3 = prefab.create_object()

    # set x and y position for the second agent
    agent2.get_component(Position).set_coordinates(tile_size, tile_size)

    state.add_game_object(agent2)
    state.add_game_object(agent3)

    renderer = Renderer(title="Agent World", window_width=window_size, window_height=window_size)

    game = Runner(renderer, event_handler, state)

    EngineLogger.setup()

    ImageCache.set_max_size(100)
    ImageCache.clear()

    game.start()


if __name__ == "__main__":
    main()
