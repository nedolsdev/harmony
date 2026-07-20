"""Sorting layer definitions for rendering order in the game."""

from __future__ import annotations

from harmony.game.error import DataAlreadyExistsError


class SortingLayer:
    """Represents a named sorting layer with a specific render order value."""

    def __init__(self, name: str, value: int, layer_id: int) -> None:
        """Initialize the sorting layer with a name, value, and unique ID."""
        self.name = name
        self.value = value
        self.id = layer_id

    def __repr__(self) -> str:
        """Return a string representation of the sorting layer."""
        return f"<SortingLayer name={self.name!r} id={self.id} value={self.value}>"

    def __eq__(self, other: object) -> bool:
        """Check equality based on unique ID."""
        return isinstance(other, SortingLayer) and self.id == other.id

    def __hash__(self) -> int:
        """Return the hash based on unique ID."""
        return hash(self.id)


class SortingLayerManager:
    """Manages sorting layers and their rendering order."""

    def __init__(self) -> None:
        """Initialize the sorting layer manager."""
        self.layers_by_id: dict[int, SortingLayer] = {}
        self.layers_by_name: dict[str, SortingLayer] = {}
        self._next_id = 1

    def create_layer(self, name: str, value: int) -> SortingLayer:
        """Create and register a new sorting layer."""
        if name in self.layers_by_name:
            msg = f"Sorting layer with name '{name}' already exists."
            raise DataAlreadyExistsError(msg)
        layer = SortingLayer(name, value, self._next_id)
        self._next_id += 1
        self.layers_by_id[layer.id] = layer
        self.layers_by_name[name] = layer
        return layer

    def get_layer(self, name: str) -> SortingLayer:
        """Retrieve a sorting layer by its name."""
        layer = self.layers_by_name.get(name)
        if layer is None:
            msg = f"Sorting layer with name '{name}' does not exist."
            raise LookupError(msg)
        return layer

    def get_layers_sorted(self) -> list[SortingLayer]:
        """Return all layers sorted by their value (render order)."""
        return sorted(self.layers_by_name.values(), key=lambda layer: layer.value)

    def remove_layer(self, name: str) -> None:
        """Remove a sorting layer by its name."""
        layer = self.layers_by_name.pop(name, None)
        if layer:
            self.layers_by_id.pop(layer.id, None)

    def get_layer_value_from_name(self, name: str) -> int:
        """Get the render order value of a layer by its name."""
        layer = self.get_layer(name)
        if not layer:
            msg = f"Sorting layer with name '{name}' does not exist."
            raise LookupError(msg)
        return layer.value
