"""The AnimationController is a state machine with transitions between animations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar, override

from core.packages.animation.clip import NO_ANIMATION, AnimationClip
from core.packages.animation.frame import AnimationFrame
from game.error import DataAlreadyExistsError, InvalidArgumentCombinationError

if TYPE_CHECKING:
    from collections.abc import Callable

    from game.object import GameObject


class StateNode:
    """A state within a StateMachine."""

    def __init__(self, name: str) -> None:
        """Initialize the StateNode with a name."""
        self.name = name

    def __str__(self) -> str:
        """Get str."""
        return self.name


NodeT = TypeVar("NodeT", bound=StateNode)
DataT = TypeVar("DataT", bound=Any)


class StateTransition[NodeT: StateNode, DataT: Any]:
    """A transition between two StateNodes."""

    def begin(
        self,
        current_state: NodeT,
        new_state: NodeT,
        resolve: Callable[[DataT], None],
        data: DataT,
    ) -> None:
        """Begin the transition between StateNodes with 'resolve' to finish the transition."""
        msg = "The 'begin' method from StateTransition is to be implemented by the subclass."
        raise NotImplementedError(msg)

    def update(self, data: DataT, resolve: Callable[[DataT], None]) -> None:
        """Update the transition, potentially calling 'resolve' to end the transition."""
        msg = "Subclasses should implement this method."
        raise NotImplementedError(msg)


class IllegalTransitionResolutionError(RuntimeError):
    """Exception raised a StateTransition is resolved while not running."""


class StateMachine[NodeT: StateNode, DataT: Any]:
    """State machine base class."""

    def __init__(self, initial_state: NodeT) -> None:
        """Initialize the StateMachine."""
        self.current_state: NodeT = initial_state
        self.transitioning_to: NodeT | None = None
        self.current_transition: StateTransition[NodeT, DataT] | None = None

        # a lookup for transitions from each node
        self.node_transitions: dict[NodeT, list[StateTransition[NodeT, DataT]]] = {}

        # a lookup for the state transition details between two nodes
        # e.g. For a transition between A -> B, we might want to look up the transition time
        self.transitions: dict[tuple[NodeT, NodeT], StateTransition[NodeT, DataT]] = {}

        # lookup from transition -> start, end
        self.start_end: dict[StateTransition[NodeT, DataT], tuple[NodeT, NodeT]] = {}

        # a lookup for all the nodes within the graph
        self.nodes: set[NodeT] = set()

        self.add_node(initial_state)

    def add_edge(self, start: NodeT, end: NodeT, transition: StateTransition[NodeT, DataT]) -> None:
        """Add a transition to the graph. Automatically adds 'start' and 'end' StateNodes if not present."""
        if self.has_transition(start, end):
            msg = f"There already exists a StateTransition between StateNodes '{start}' and '{end}'"
            raise DataAlreadyExistsError(msg)

        # add nodes if they don't exist
        if not self.has_node(start):
            self.add_node(start)
        if not self.has_node(end):
            self.add_node(end)

        # add the transition
        self.transitions[(start, end)] = transition
        self.start_end[transition] = (start, end)

        self.node_transitions[start].append(transition)

    def has_transition(self, start: NodeT, end: NodeT) -> bool:
        """Check whether the StateMachine has an existing transition between two StateNodes."""
        return self.transitions.get((start, end), None) is not None

    def add_node(self, node: NodeT) -> None:
        """Add a StateNode to the StateMachine. The StateNode does not necessarily have to be attached to the graph."""
        self.nodes.add(node)
        self.node_transitions[node] = []

    def has_node(self, node: NodeT) -> bool:
        """Check whether the StateNode exists within the StateMachine."""
        return node in self.nodes

    def remove_node(self, node: NodeT) -> None:
        """Remove a StateNode from the StateMachine, disconnecting any existing StateTransitions."""
        self.nodes.remove(node)

        del self.node_transitions[node]

        # copy so that we can delete safely and still fully iter
        transitions = self.transitions.copy()

        for transition in transitions:
            start, end = transition

            if node in (start, end):
                del self.start_end[self.transitions[(start, end)]]
                del self.transitions[(start, end)]

    def remove_edge(self, start: NodeT, end: NodeT) -> None:
        """Remove an edge between two StateNodes from the StateMachine."""
        if self.has_transition(start, end):
            del self.transitions[(start, end)]

    def remove_transition(self, transition: NodeT) -> None:
        """Remove an edge (as a StateTransition) from the StateMachine."""
        for start, end in self.transitions:
            if self.transitions[(start, end)] == transition:
                self.remove_edge(start, end)
                return

        msg = f"StateMachine does not contain StateTransition '{transition}'"
        raise LookupError(msg)

    def is_in_transition(self) -> bool:
        """Check whether the StateMachine is transitioning between StateNodes."""
        return self.transitioning_to is not None

    def transition_to(self, new_state: NodeT, data: DataT) -> None:
        """Start transitioning to a new StateNode."""
        # check there is a valid transition between nodes
        if not self.has_transition(self.current_state, new_state):
            msg = f"There is no valid StateTransition between '{self.current_state}' and '{new_state}'"
            raise LookupError(msg)

        self.transitioning_to = new_state
        transition = self.transitions[(self.current_state, new_state)]
        self.current_transition = transition
        transition.begin(self.current_state, new_state, self.resolve_transition, data)

    def resolve_transition(self, data: DataT) -> None:  # noqa: ARG002
        """Finish the current StateTransition marking the targeted state as the current state."""
        if not self.is_in_transition():
            msg = "Cannot resolve transition as the StateMachine is not performing a StateTransition."
            raise IllegalTransitionResolutionError(msg)

        self.current_state = self.transitioning_to  # pyright: ignore[reportAttributeAccessIssue] (we can guarantee self.transition_to is not None)
        self.transitioning_to = None
        self.current_transition = None

    def find_node(self, name: str) -> NodeT | None:
        """Find the node with a given name."""
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_transitions_from_node(self, node: NodeT) -> list[StateTransition[NodeT, DataT]]:
        """Get the transitions from a particular node."""
        return self.node_transitions[node]


FrameT = TypeVar("FrameT", bound=AnimationFrame)


class AnimationState[FrameT: AnimationFrame](StateNode):
    """Node for an animation state within an AnimationLayer state machine."""

    def __init__(self, name: str, clip: AnimationClip[FrameT]) -> None:
        """Initialize the AnimationState with a name and associated AnimationClip."""
        super().__init__(name)
        self.clip = clip


class AnimationTransition[DataT: Any, FrameT: AnimationFrame](StateTransition[AnimationState[FrameT], DataT]):
    """A transition between two StateNodes in the AnimationController."""

    def __init__(self, condition: Callable[[DataT], bool] | None = None) -> None:
        """Initialize the AnimationTransition."""
        super().__init__()

        def no_condition(data: DataT) -> bool:  # noqa: ARG001 (need correct number of args for typing)
            """Automatically pass."""
            return True

        self.condition = condition or no_condition

    @override
    def begin(
        self,
        current_state: AnimationState[FrameT],
        new_state: AnimationState[FrameT],
        resolve: Callable[[DataT], None],
        data: DataT,
    ) -> None:
        """Begin the transition between StateNodes with 'resolve' to finish the transition."""
        # for now, just immediately resolve
        # TODO: Resolve based on exit_time or other  # noqa: TD003
        resolve(data)


ENTRY_STATE = AnimationState("ENTRY", NO_ANIMATION)


class AnimationLayer(StateMachine[AnimationState, Generic[DataT]]):
    """The AnimationLayer is a state machine with transitions between animations."""

    def __init__(
        self,
        name: str,
        initial_state: AnimationState = ENTRY_STATE,
    ) -> None:
        """Initialize the AnimationLayer with a name."""
        super().__init__(initial_state=initial_state)
        self.name = name

    def update(self, data: DataT, target: GameObject) -> None:
        """Update the AnimationLayer."""
        # if we are in transition progress the transition
        if self.is_in_transition() and self.current_transition:
            self.current_transition.update(data, self.resolve_transition)
            return

        # otherwise we will check if we can transition to a new animation
        transitions = self.get_transitions_from_node(self.current_state)

        # check if we can transition
        for transition in transitions:
            # TODO: Fix this hack  # noqa: TD003
            # bit scuffed but we force transition to be the correct type
            assert isinstance(transition, AnimationTransition)  # noqa: S101

            if transition.condition(data):
                # immediately exit, we can't to transition to multiple states
                _, end = self.start_end[transition]

                self.transition_to(end, data)
                break

        # continue with our animation
        self.update_clip(self.current_state.clip, target)

    def update_clip(self, clip: AnimationClip, target: GameObject) -> None:
        """Update the current animation clip."""
        frame = clip.get_next_animation_frame()

        # end of the animation don't do anything
        # if there is no clip target component we can't render it
        if frame is None or clip.target is None:
            return

        component_type = clip.target.component_type

        # apply the animation frame
        target.set_animation_frame(frame, clip.target, component_type)


class AnimationController[DataT: Any]:
    """The AnimationController controls the layer and parameters passed to the layers for state transitions."""

    def __init__(self, data: DataT, *, init_default_layer: bool = True) -> None:
        """Initialize the AnimationController."""
        self.data = data
        self.layers: list[AnimationLayer] = []

        if init_default_layer:
            # create default layer
            default_layer = AnimationLayer("default")
            self.layers.append(default_layer)

    def get_layer(self, *, index: int = 0, name: str | None = None) -> AnimationLayer:
        """Get a specific layer by index or name in the AnimationController. Defaults as the first layer."""
        if index is not None and name is not None:
            msg = "Invalid parameters. Only set one of 'index' or 'name'."
            raise InvalidArgumentCombinationError(msg)

        if name is not None:
            for layer in self.layers:
                if layer.name == name:
                    return layer
            msg = f"Could not find AnimationLayer with name '{name}'."
            raise LookupError(msg)

        return self.layers[index]

    def add_layer(self, layer: AnimationLayer) -> None:
        """Add a layer."""
        self.layers.append(layer)

    def update(self, target: GameObject) -> None:
        """Update the AnimationLayers of the controller."""
        for layer in self.layers:
            layer.update(self.data, target)
