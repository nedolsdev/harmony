"""Main entry point for the Agent World game."""

from game.draw import Renderer
from game.event_handler import EventHandler
from game.runner import Runner
from world.state import GameState


def main() -> None:
    """Initialize the game and start the renderer."""
    state = GameState()
    renderer = Renderer(state.grid.GRID_SIZE)
    event_handler = EventHandler()

    game = Runner(renderer, event_handler, state)

    game.start()


if __name__ == "__main__":
    main()
