from __future__ import annotations


class Position:
    """
    The Position class defines a specific position (x,y) in the environment.
    """
    def __init__(
            self,
            x: int = -1,
            y: int = -1) -> None:
        self.x = x
        self.y = y

    def __eq__(
            self,
            other: Position) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(
            self) -> str:
        return str((self.x, self.y))
