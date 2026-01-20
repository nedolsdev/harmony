"""The AnimationController is a state machine with transitions between animations."""

from collections.abc import Callable


class StateNode:
    """A state within a StateMachine."""

    def __init__(self, name: str) -> None:
        """Initialize the StateNode with a name."""
        self.name = name


class StateTransition:
    """A transition between two StateNodes."""

    def begin(self, current_state: StateNode, new_state: StateNode, resolve: Callable[[], None]) -> None:
        """Begin the transition between StateNodes with 'resolve' to finish the transition."""
        msg = "The 'begin' method from StateTransition is to be implemented by the subclass."
        raise NotImplementedError(msg)


class StateMachine:
    """State machine base class."""

    def __init__(self, initial_state: StateNode) -> None:
        """Initialize the StateMachine."""
        self.current_state: StateNode = initial_state
        self.transitioning_to: StateNode | None = None

        # a directed graph for connections between Nodes
        # e.g. "Node A": "Node B" means A -> B
        self.graph: dict[StateNode, StateNode] = {}

        # a lookup for the state transition details between two nodes
        # e.g. For a transition between A -> B, we might want to look up the transition time
        self.transitions: dict[tuple[StateNode, StateNode], StateTransition] = {}

        # a lookup for all the nodes within the graph
        self.nodes: set[StateNode] = set()

    def add_edge(self, start: StateNode, end: StateNode, transition: StateTransition) -> None:
        """Add a transition to the graph. Automatically adds 'start' and 'end' StateNodes if not present."""
        if self.has_transition(start, end):
            msg = f"There already exists a StateTransition between StateNodes '{start}' and '{end}'"
            raise ValueError(msg)

        # add nodes if they don't exist
        if not self.has_node(start):
            self.add_node(start)
        if not self.has_node(end):
            self.add_node(end)

        # add the transition
        self.transitions[(start, end)] = transition

    def has_transition(self, start: StateNode, end: StateNode) -> bool:
        """Check whether the StateMachine has an existing transition between two StateNodes."""
        return self.transitions.get((start, end), None) is not None

    def add_node(self, node: StateNode) -> None:
        """Add a StateNode to the StateMachine. The StateNode does not necessarily have to be attached to the graph."""
        self.nodes.add(node)

    def has_node(self, node: StateNode) -> bool:
        """Check whether the StateNode exists within the StateMachine."""
        return node in self.nodes

    def remove_node(self, node: StateNode) -> None:
        """Remove a StateNode from the StateMachine, disconnecting any existing StateTransitions."""
        self.nodes.remove(node)

        for start, end in self.graph.items():
            if node in (start, end):
                # remove transition to or from deleted node
                del self.transitions[(start, end)]
                # remove any connections on the graph from or to the removed node
                del self.graph[start]

    def remove_edge(self, start: StateNode, end: StateNode) -> None:
        """Remove an edge between two StateNodes from the StateMachine."""
        if self.has_transition(start, end):
            del self.transitions[(start, end)]

    def remove_transition(self, transition: StateTransition) -> None:
        """Remove an edge (as a StateTransition) from the StateMachine."""
        for start, end in self.transitions:
            if self.transitions[(start, end)] == transition:
                self.remove_edge(start, end)
                return

        msg = f"StateMachine does not contain StateTransition '{transition}'"
        raise ValueError(msg)

    def is_in_transition(self) -> bool:
        """Check whether the StateMachine is transitioning between StateNodes."""
        return self.transitioning_to is not None

    def transition_to(self, new_state: StateNode) -> None:
        """Start transitioning to a new StateNode."""
        # check there is a valid transition between nodes
        if not self.has_transition(self.current_state, new_state):
            msg = f"There is no valid StateTransition between '{self.current_state}' and '{new_state}'"
            raise ValueError(msg)

        self.transitioning_to = new_state
        transition = self.transitions[(self.current_state, new_state)]
        transition.begin(self.current_state, new_state, self.resolve_transition)

    def resolve_transition(self) -> None:
        """Finish the current StateTransition marking the targeted state as the current state."""
        if not self.is_in_transition():
            msg = "Cannot resolve transition as the StateMachine is not performing a StateTransition."
            raise ValueError(msg)

        self.current_state = self.transitioning_to  # pyright: ignore[reportAttributeAccessIssue] (we can guarantee self.transition_to is not None)
        self.transitioning_to = None


class AnimationController(StateMachine):
    """AnimationController is a state machine with transitions between animations."""

    def __init__(self, initial_state: StateNode | None = None) -> None:
        """Initialize the AnimationController. If no initial state is given, a default idle empty animation is made."""
        super().__init__(initial_state or StateNode("Idle"))
