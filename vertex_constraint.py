from __future__ import annotations
from position import Position


class VertexConstraint:
    """
    A vertex constraint is constraint which defines a vertex to be added in the
    top-level CBS tree.
    """
    def __init__(
            self,
            time: int,
            position: Position) -> None:
        self.time = time
        self.position = position

    def __eq__(
            self,
            other: VertexConstraint) -> bool:
        return self.time == other.time and self.position == other.position

    def __hash__(
            self) -> hash:
        """Added to make this class hashable"""
        return hash(str(self.time)+str(self.position.x) + str(self.position.y))

    def __str__(
            self) -> str:
        return '[' + str(self.time) + ', ' + str(self.position) + ']'
