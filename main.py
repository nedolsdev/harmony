"""Main entry point for the Agent World game."""

from core.agent import Agent
from game.draw import Renderer
from game.event_handler import EventHandler
from game.runner import Runner
from world.state import GameState


def main() -> None:
    """Initialize the game and start the renderer."""
    state = GameState()
    event_handler = EventHandler()

    agent = Agent(event_handler, position=(0, 0), width=60, height=60)
    state.add_game_object(agent)

    renderer = Renderer(state.grid.GRID_SIZE)

    game = Runner(renderer, event_handler, state)

    game.start()


if __name__ == "__main__":
    main()
