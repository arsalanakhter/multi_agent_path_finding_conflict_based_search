from __future__ import annotations
from position import Position


class State:
    """
    The State class defines the state of an agent at a specific time. This
    includes both the position and time for that agent
    """

    def __init__(
            self,
            time: int,
            position: Position) -> None:
        self.position = position
        self.time = time

    def __eq__(
            self,
            other: State) -> bool:
        return self.time == other.time and self.position == other.position

    def is_equal_except_time(
            self,
            other: State) -> bool:
        return self.position == other.position

    def __hash__(
            self) -> hash:
        """Added to make the State class hashable"""
        return hash(str(self.time)+str(self.position.x) + str(self.position.y))

    def __str__(
            self) -> str:
        return str((self.time, self.position.x, self.position.y))
