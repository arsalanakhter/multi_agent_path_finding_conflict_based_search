from __future__ import annotations
from position import Position


class EdgeConstraint:
    """
    An edge constraint is constraint which defines an edge to be added in the
    top-level CBS tree.
    """
    def __init__(
            self,
            time: int,
            position_1: Position,
            position_2: Position):
        self.time = time
        self.position_1 = position_1
        self.position_2 = position_2

    def __eq__(
            self,
            other: EdgeConstraint) -> bool:
        return self.time == other.time and self.position_1 == other.position_1 \
            and self.position_2 == other.position_2

    def __hash__(
            self) -> hash:
        """Added to make this class hashable"""
        return hash(str(self.time)+str(self.position_1) + str(self.position_2))

    def __str__(
            self) -> str:
        return '[' + str(self.time) + ', (' + str(self.position_1) + ', ' + \
            str(self.position_2) + ')]'
