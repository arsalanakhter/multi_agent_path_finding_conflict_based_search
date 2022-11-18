from __future__ import annotations


class Constraints:
    """
    Used to add the constraints to the top-level CBS tree.
    """
    def __init__(
            self) -> None:
        self.vertex_constraints = set()
        self.edge_constraints = set()

    def add_constraint(
            self,
            other: Constraints) -> None:
        self.vertex_constraints |= other.vertex_constraints
        self.edge_constraints |= other.edge_constraints

    def __str__(
            self) -> str:
        return "VC: " + str([str(vc) for vc in self.vertex_constraints]) + \
            "EC: " + str([str(ec) for ec in self.edge_constraints])
