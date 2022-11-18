class AStar:
    """
    Define the A-star class for low-level shortest path computation
    """

    def __init__(
            self,
            env) -> None:
        self.agent_dict = env.agent_dict
        self.admissible_heuristic = env.admissible_heuristic
        self.is_at_goal = env.is_at_goal
        self.get_neighbors = env.get_neighbors

    @staticmethod
    def reconstruct_path(
            came_from,
            current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def search(self, agent_name):
        """
        low level search
        """
        initial_state = self.agent_dict[agent_name]["start"]
        step_cost = 1

        closed_set = set()
        # Open_set is the set of nodes that need to be expanded / re-expanded
        open_set = {initial_state}

        # came_from is the node/state that immediately precedes the current
        # node/state on the shortest path from the start to the currently known
        # node/state
        came_from = {}

        # g_score is the cost of the cheapest path from start node/state to
        # current node/state
        g_score = {initial_state: 0}

        # For node n, fScore[n] := gScore[n] + h(n), where h(n) represents
        # the admissible heuristic. It is our best guess of the cost of the
        # path if it goes through n
        f_score = {initial_state: self.admissible_heuristic(initial_state,
                                                            agent_name)}

        while open_set:
            # Initialize the temp dict
            temp_dict = {
                open_item: f_score.setdefault(open_item, float("inf")) for
                open_item in open_set}
            current = min(temp_dict, key=temp_dict.get)

            if self.is_at_goal(current, agent_name):
                return self.reconstruct_path(came_from, current)

            open_set -= {current}
            closed_set |= {current}

            neighbor_list = self.get_neighbors(current)

            for neighbor in neighbor_list:
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score.setdefault(current, float(
                    "inf")) + step_cost

                if neighbor not in open_set:
                    open_set |= {neighbor}
                elif tentative_g_score >= g_score.setdefault(neighbor,
                                                             float("inf")):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[
                                        neighbor] + self.admissible_heuristic(
                    neighbor, agent_name)
        return False
