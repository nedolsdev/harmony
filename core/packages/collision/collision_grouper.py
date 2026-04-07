"""Groups objects that should check collisions with each other."""
from __future__ import annotations


class CollisionGrouper:
    """Groups objects that should check collisions with each other."""


class QuadTreeGrouper(CollisionGrouper):
    """Groups collision objects using a QuadTree."""


class CoarseGridGrouper(CollisionGrouper):
    """Groups collision objects based on a grid with pre-defined cell sizes."""


# basically a grouper's role is to reduce the number of checks for a given CollisionRule
# so we get a bunch of pairs back from the CollisionRule
# so what we want to do
# is essentially created CollisionLayers on the fly
# and our own CollisionRules on the fly
