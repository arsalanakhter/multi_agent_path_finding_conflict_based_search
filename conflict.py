from __future__ import annotations
from position import Position


class Conflict:
    """
    The Conflict class defines what kind of conflicts can occur for two agents.
    There are many kinds of conflicts that can occur, including vertex, edge,
    cycle and swapping conflicts.

    We only consider two kinds of conflicts in the current implementation, a
    vertex conflict and an edge conflict.

    A vertex conflict is a conflict where agents plan to occupy the same vertex
    at the same time stamp.

    An edge conflict occurs when agents plan to traverse the same edge at the
    same time stamp.
    """
    VERTEX = 1
    EDGE = 2

    def __init__(
            self) -> None:
        self.time = -1
        self.conflict_type = -1

        self.agent_1 = ''
        self.agent_2 = ''

        self.position_1 = Position()
        self.position_2 = Position()

    def __str__(self):
        return '[' + str(self.time) + ', ' + self.agent_1 + ', ' + self.agent_2 + \
               ', (' + str(self.position_1) + ', ' + str(self.position_2) + ')' + ']'
