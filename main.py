"""Main entry point for the Agent World game."""

from agent_world.agent import Agent
from agent_world.components.movement import Movement
from core.components.position import Position
from core.objects.grid import GridGenerator
from game.draw import Renderer
from game.event_handler import EventHandler
from game.runner import Runner
from game.state import GameState


def main() -> None:
    """Initialize the game and start the renderer."""
    state = GameState()
    event_handler = EventHandler()

    grid = GridGenerator.generate(grid_size=10)
    state.add_game_object(grid)

    agent = Agent(position=(0, 0), width=60, height=60)
    state.add_game_object(agent)
    agent.add_component(Movement(position=agent.get_component(Position), grid=grid))

    renderer = Renderer(grid_size=10)

    game = Runner(renderer, event_handler, state)

    game.start()


if __name__ == "__main__":
    main()
