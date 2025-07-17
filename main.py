"""Main entry point for the Agent World game."""

from agent_world.components.movement import Movement
from agent_world.objects.agent import Agent
from core.components.grid_render import GridRender
from core.objects.grid import GridGenerator
from game.draw import Renderer
from game.event_handler import EventHandler
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

    agent = Agent(position=(0, 0), width=tile_size, height=tile_size)
    state.add_game_object(agent)
    agent.add_component(Movement(grid))

    renderer = Renderer(title="Agent World", window_width=window_size, window_height=window_size)

    game = Runner(renderer, event_handler, state)

    game.start()


if __name__ == "__main__":
    main()
