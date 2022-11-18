from __future__ import annotations


class HighLevelNode(object):
    """
    Root node for CBS
    """
    def __init__(self) -> None:
        self.solution = {}
        self.constraint_dict = {}
        self.cost = 0

    def __eq__(
            self,
            other: HighLevelNode) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.solution == other.solution and self.cost == other.cost

    def __hash__(
            self) -> hash:
        """Added to make this class hashable"""
        return hash(self.cost)

    def __lt__(       # Less than
            self,
            other: HighLevelNode):
        return self.cost < other.cost
