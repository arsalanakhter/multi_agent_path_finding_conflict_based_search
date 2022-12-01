# A basic implementation of the Conflict-Based Search (CBS) for the Multi-Agent
# Path Finding (MAPF) Problem. The problem is to find a path for multiple
# robots such that they could go through the shared pathways without having
# a conflict with each other.
#
# This implementation is inspired by multiple repos, as follows:
# - https://github.com/gloriyo/MAPF-ICBS
# - https://github.com/nicofretti/MAPF
# The code in this implementation is heavily influenced by the following work:
# - https://github.com/jainaviral898/mapp-cbs-aifa
#
# Couple of notes/observations
# - This is a basic implementation of CBS. Multiple improvement approaches
# exist for CBS, which I further plan to explore. These include
# CBS + Disjoint Splitting
# CBS + High Level Heuristics
# CBS + Prioritising Conflicts
# The last one is what I do plan to explore a bit next, since it seems to have
# better performance, based on a graph in a report here:
# https://github.com/polinko13/CBS/blob/main/cbs_report.pdf
# However, Other implementations also exist and the newer variants are worth
# looking into.
# - It appears a C++ implementation may result in a speedup. I also plan to
# explore that avenue
# - CBS based approaches are one way to solve the problem. Other approaches
# include Priority based planning as well as Constraint programming or
# Mixed-Integer programming (MIP) based approaches. Some are more focussed on
# path optimality, such as MIPs, and some on speed, such as priority-based
# approaches.
#
# Author - Arsalan Akhter


from itertools import zip_longest
from pogema import pogema_v0, GridConfig
from pogema.animation import AnimationMonitor

from environment import Environment
from cbs import CBS


def extract_moves_from_solution(solution):
    # Actions
    WAIT = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    moves = []
    single_move = []
    for r_ID, sol in solution.items():
        for s1, s2 in zip(sol[:-1], sol[1:]):
            _, q1 = s1
            x1, y1 = q1
            _, q2 = s2
            x2, y2 = q2

            if x2 == x1 and y2 == y1:
                single_move.append(WAIT)
            elif x2 == x1 + 1 and y2 == y1:
                single_move.append(RIGHT)
            elif x2 == x1 - 1 and y2 == y1:
                single_move.append(LEFT)
            elif x2 == x1 and y2 == y1 + 1:
                single_move.append(UP)
            elif x2 == x1 and y2 == y1 - 1:
                single_move.append(DOWN)
            else:
                raise ValueError("Wrong Move detected!")
        moves.append(single_move)
        single_move = []
    # Make them step moves for all agents at one step
    moves2 = [list(i) for i in zip_longest(*moves, fillvalue=0)]
    return moves2


def main():
    # grid = """
    # B##A
    # ....
    # a##b
    # """

    grid = """
    ........
    B######A
    .######.
    .######.
    ........
    .######.
    .######.
    a######b
    ........
    """

    # Define new configuration
    grid_config = GridConfig(map=grid)

    # Create custom Pogema-based arena
    arena = pogema_v0(grid_config=grid_config)

    # Render the arena
    # arena.reset()
    # arena.render()
    # Extract the relevant parameters from grid_config
    arena_map = grid_config.map

    # Create an environment dict for input to the environment class
    # Assuming a 2-dimensional grid
    env_dict = {'dimensions': (len(arena_map), len(arena_map[0])),
                'arena_map': arena_map,
                'obstacles': [(idx, idx2) for idx, i in enumerate(arena_map)
                              for idx2, j in enumerate(i) if j == 1],
                'agents': [{'name': 'R_' + str(i),
                            'start': tuple(grid_config.agents_xy[i]),
                            'goal': tuple(grid_config.targets_xy[i])}
                           for i in range(grid_config.num_agents)]
                }
    cbs_env = Environment(env_dict)
    # Searching
    cbs = CBS(cbs_env)
    solution = cbs.search()
    if not solution:
        print(" Solution not found")
    # print('Solution Template: (time-step, (x, y))')
    # print(solution)

    # For Animation
    arena = AnimationMonitor(arena)
    arena.reset()
    steps = extract_moves_from_solution(solution)
    # Convert the agent results back to steps for pogema to render
    for step in steps:
        obs, reward, done, info = arena.step(step)

    arena.save_animation("render.svg")


if __name__ == "__main__":
    main()
