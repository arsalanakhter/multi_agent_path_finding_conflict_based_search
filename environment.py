from __future__ import annotations
from position import Position
from state import State
from vertex_constraint import VertexConstraint
from edge_constraint import EdgeConstraint
from constraints import Constraints
from conflict import Conflict
from itertools import combinations
from math import fabs
from a_star import AStar


class Environment:
    """
    Orchestration of CBS happens here.
    """

    def __init__(
            self,
            env_dict: dict) -> None:
        self.dimension = env_dict['dimensions']
        self.obstacles = env_dict['obstacles']

        self.agents = env_dict['agents']
        self.agent_dict = {}

        self.make_agent_dict()

        self.constraints = Constraints()
        self.constraint_dict = {}

        self.a_star = AStar(self)

    def get_neighbors(
            self,
            state: State) -> list:
        """
        Extract neighbours valid for the next move. The valid moves include
        wait, up, down, left and right

        :param state: The current state of the agent
        :returns: A list of neighbours valid for the next move
        """

        neighbors = []
        # Wait action
        n = State(state.time + 1, state.position)
        if self.is_state_valid(n):
            neighbors.append(n)
        # Up action
        n = State(state.time + 1, Position(state.position.x,
                                           state.position.y + 1))
        if self.is_state_valid(n) and self.is_transition_valid(state, n):
            neighbors.append(n)
        # Down action
        n = State(state.time + 1, Position(state.position.x,
                                           state.position.y - 1))
        if self.is_state_valid(n) and self.is_transition_valid(state, n):
            neighbors.append(n)
        # Left action
        n = State(state.time + 1, Position(state.position.x - 1,
                                           state.position.y))
        if self.is_state_valid(n) and self.is_transition_valid(state, n):
            neighbors.append(n)
        # Right action
        n = State(state.time + 1, Position(state.position.x + 1,
                                           state.position.y))
        if self.is_state_valid(n) and self.is_transition_valid(state, n):
            neighbors.append(n)
        return neighbors

    def get_first_conflict(
            self,
            solution) -> Conflict:
        """
        Extract the first conflict that exists in the plans

        :param solution: Complete solution containing plans for each agent
        :returns: An object of type Conflict, containing the first conflict
                    found
        """
        max_t = max([len(plan) for plan in solution.values()])
        result = Conflict()

        for t in range(max_t):
            # Identify a vertex conflict
            for agent_1, agent_2 in combinations(solution.keys(), 2):
                state_1 = self.get_state(agent_1, solution, t)
                state_2 = self.get_state(agent_2, solution, t)
                if state_1.is_equal_except_time(state_2):
                    result.time = t
                    result.conflict_type = Conflict.VERTEX
                    result.position_1 = state_1.position
                    result.agent_1 = agent_1
                    result.agent_2 = agent_2
                    return result

            # Identify an edge conflict
            for agent_1, agent_2 in combinations(solution.keys(), 2):
                state_1a = self.get_state(agent_1, solution, t)
                state_1b = self.get_state(agent_1, solution, t + 1)

                state_2a = self.get_state(agent_2, solution, t)
                state_2b = self.get_state(agent_2, solution, t + 1)

                if state_1a.is_equal_except_time(
                        state_2b) and state_1b.is_equal_except_time(state_2a):
                    result.time = t
                    result.conflict_type = Conflict.EDGE
                    result.agent_1 = agent_1
                    result.agent_2 = agent_2
                    result.position_1 = state_1a.position
                    result.position_2 = state_1b.position
                    return result
        return None

    def create_constraints_from_conflict(
            self,
            conflict: Conflict) -> dict:
        """
        Creates the constraints that need to be added to the CBS tree

        :param conflict: The conflict that has been identified
        :returns: A dict containing constraints
        """
        constraint_dict = {}
        if conflict.conflict_type == Conflict.VERTEX:
            v_constraint = VertexConstraint(conflict.time, conflict.position_1)
            constraint = Constraints()
            constraint.vertex_constraints |= {v_constraint}
            constraint_dict[conflict.agent_1] = constraint
            constraint_dict[conflict.agent_2] = constraint

        elif conflict.conflict_type == Conflict.EDGE:
            constraint1 = Constraints()
            constraint2 = Constraints()

            e_constraint1 = EdgeConstraint(conflict.time, conflict.position_1,
                                           conflict.position_2)
            e_constraint2 = EdgeConstraint(conflict.time, conflict.position_2,
                                           conflict.position_1)

            constraint1.edge_constraints |= {e_constraint1}
            constraint2.edge_constraints |= {e_constraint2}

            constraint_dict[conflict.agent_1] = constraint1
            constraint_dict[conflict.agent_2] = constraint2

        return constraint_dict

    def get_state(
            self,
            agent_name,
            solution,
            t):
        if t < len(solution[agent_name]):
            return solution[agent_name][t]
        else:
            return solution[agent_name][-1]

    def is_state_valid(
            self,
            state: State) -> bool:
        """
        Checks if a state is valid or not.
        :param state: State to be checked
        :returns: bool, whether the state is valid or not
        """
        return state.position.x >= 0 and state.position.x < self.dimension[0] \
               and state.position.y >= 0 and state.position.y < self.dimension[1] \
               and VertexConstraint(state.time, state.position) not in self.constraints.vertex_constraints \
               and (state.position.x, state.position.y) not in self.obstacles

    def is_transition_valid(
            self,
            state_1: State,
            state_2: State) -> bool:
        """
        Checks if a state is valid or not.
        :param state_1: State to be checked
        :param state_2: State to be checked
        :returns: bool, whether the state is valid or not
        """
        return EdgeConstraint(state_1.time, state_1.position,
                              state_2.position) not in self.constraints.edge_constraints

    def is_solution(self, agent_name):
        pass

    def admissible_heuristic(
            self,
            state,
            agent_name):
        goal = self.agent_dict[agent_name]["goal"]
        return fabs(state.position.x - goal.position.x) + \
               fabs(state.position.y - goal.position.y)

    def is_at_goal(
            self,
            state: State,
            agent_name) -> bool:
        goal_state = self.agent_dict[agent_name]["goal"]
        return state.is_equal_except_time(goal_state)

    def make_agent_dict(self):
        for agent in self.agents:
            start_state = State(0, Position(agent['start'][0], agent['start'][1]))
            goal_state = State(0, Position(agent['goal'][0], agent['goal'][1]))
            self.agent_dict.update({agent['name']: {'start': start_state, 'goal': goal_state}})

    def compute_solution(self):
        solution = {}
        for agent in self.agent_dict.keys():
            self.constraints = self.constraint_dict.setdefault(agent, Constraints())
            local_solution = self.a_star.search(agent)
            if not local_solution:
                return False
            solution.update({agent: local_solution})
        return solution

    def compute_solution_cost(
            self,
            solution):
        return sum([len(path) for path in solution.values()])
