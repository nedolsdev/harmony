"""Main entry point for the Agent World game."""

import pygame

from core.agent import Agent
from game.draw import Renderer
from game.event import PygameKeydownEvent
from game.event_handler import EventHandler
from game.runner import Runner
from world.state import GameState


def main() -> None:
    """Initialize the game and start the renderer."""
    state = GameState()

    agent = Agent((0, 0), width=60, height=60)
    state.add_game_object(agent)

    renderer = Renderer(state.grid.GRID_SIZE)
    event_handler = EventHandler()

    game = Runner(renderer, event_handler, state)

    # TODO: Refactor agent event listeners out of main.py
    # https://github.com/theneddlesking/agent-world/issues/1

    # add movement listeners
    event_handler.register_listener(
        PygameKeydownEvent.get_name_from_key(pygame.K_UP),
        lambda _, __: agent.move_up(),
    )
    event_handler.register_listener(
        PygameKeydownEvent.get_name_from_key(pygame.K_DOWN),
        lambda _, __: agent.move_down(),
    )
    event_handler.register_listener(
        PygameKeydownEvent.get_name_from_key(pygame.K_LEFT),
        lambda _, __: agent.move_left(),
    )
    event_handler.register_listener(
        PygameKeydownEvent.get_name_from_key(pygame.K_RIGHT),
        lambda _, __: agent.move_right(),
    )

    game.start()


if __name__ == "__main__":
    main()
