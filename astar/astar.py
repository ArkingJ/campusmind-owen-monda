"""A* search on the CampusMind map, using a hop-count heuristic.

Run:  python3 astar.py                    (Main Gate to Science Lab)
      python3 astar.py "Library" "Cafeteria"
Add --quiet to hide the step-by-step trace.
"""
import heapq
import itertools
import sys
from collections import deque

CAMPUS = {
    "Main Gate":            [("Administration Block", 1), ("Cafeteria", 3)],
    "Administration Block": [("Main Gate", 1), ("Library", 2), ("Science Lab", 2)],
    "Library":              [("Administration Block", 2)],
    "Science Lab":          [("Administration Block", 2), ("Student Affairs", 2)],
    "Student Affairs":      [("Cafeteria", 2), ("Science Lab", 2)],
    "Cafeteria":            [("Main Gate", 3), ("Student Affairs", 2)],
}


def hops_to(goal):
    """Heuristic table: fewest connections from every location to the goal.

    Costs are ignored on purpose. Every connection costs at least 1 km, so the
    real distance is never smaller than the number of connections. That is why
    this guess never overestimates (it is admissible).
    """
    hops = {goal: 0}
    queue = deque([goal])
    while queue:
        node = queue.popleft()
        for neighbour, _km in CAMPUS[node]:
            if neighbour not in hops:
                hops[neighbour] = hops[node] + 1
                queue.append(neighbour)
    return hops


def astar(start, goal, trace=True):
    h = hops_to(goal)
    tie = itertools.count()            # breaks ties so heapq never compares paths
    # Frontier entries: (f, tie, g, path).  f = g + h
    frontier = [(h[start], next(tie), 0, [start])]
    best_g = {start: 0}                # cheapest known cost to reach each place
    closed = set()                     # places already expanded
    expanded = 0

    while frontier:
        if trace:
            shown = sorted((f, p[-1], g) for f, _t, g, p in frontier)
            print("frontier:", ["%s(g=%d,h=%d,f=%d)" % (n, g, h[n], f)
                                for f, n, g in shown])
        f, _t, g, path = heapq.heappop(frontier)   # lowest f first
        node = path[-1]
        if node in closed:
            continue
        closed.add(node)
        expanded += 1
        if trace:
            print("  expand :", node)

        if node == goal:               # goal test happens when popped
            return path, g, expanded

        for neighbour, km in CAMPUS[node]:
            new_g = g + km
            if neighbour not in best_g or new_g < best_g[neighbour]:
                best_g[neighbour] = new_g
                heapq.heappush(frontier, (new_g + h[neighbour], next(tie),
                                          new_g, path + [neighbour]))
    return None, None, expanded


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start = args[0] if args else "Main Gate"
    goal = args[1] if len(args) > 1 else "Science Lab"
    if start not in CAMPUS or goal not in CAMPUS:
        sys.exit("Unknown location. Choose from: " + ", ".join(CAMPUS))

    print("Heuristic (hops to %s): %s" % (goal, hops_to(goal)))
    print()
    path, cost, expanded = astar(start, goal, trace="--quiet" not in sys.argv)
    print()
    print("A* path  :", " -> ".join(path))
    print("Cost     :", cost, "km")
    print("Hops     :", len(path) - 1)
    print("Expanded :", expanded)
