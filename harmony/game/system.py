"""A system part of the game engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from harmony.game.component import GameComponent
    from harmony.game.component_channel import ComponentChannel
    from harmony.game.component_manager import ComponentManager


class System:
    """A system part of the game engine."""

    def __init__(self) -> None:
        """Initialize the ComponentSystem."""
        self._channels: dict[type[GameComponent], ComponentChannel] = {}

    def _add_channel[T: GameComponent](
        self,
        component_type: type[T],
        component_manager: ComponentManager,
    ) -> ComponentChannel[T]:
        """Add a channel if it doesn't exist yet for a particular component type."""
        channel = component_manager.add_channel(component_type)
        self._channels[component_type] = channel
        return channel

    def pre_init(self) -> None:
        """Before initialization of the system."""

    def init(self) -> None:
        """Initialize the system."""

    def pre_update(self) -> None:
        """Pre-update the system."""

    def update(self) -> None:
        """Update the system."""

    def fixed_update(self) -> None:
        """Update the system on fixed physics step."""

    def late_update(self) -> None:
        """Late update the system."""

    def post_update(self) -> None:
        """Post update the system."""
