"""Main entry point for the Agent World game."""

from __future__ import annotations

from rich.traceback import install

from evolution_game.game import create_evolution_game

install()


def main() -> None:
    """Initialize the game and start the renderer."""
    game = create_evolution_game()
    game.start()


if __name__ == "__main__":
    main()
