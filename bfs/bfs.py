"""Breadth-first search on the CampusMind map.

Run:  python3 bfs.py                      (Main Gate to Science Lab)
      python3 bfs.py "Library" "Cafeteria"
Add --quiet to hide the step-by-step trace.
"""
import sys
from collections import deque

# Each location lists its neighbours as (neighbour, km). Roads work both ways.
CAMPUS = {
    "Main Gate":            [("Administration Block", 1), ("Cafeteria", 3)],
    "Administration Block": [("Main Gate", 1), ("Library", 2), ("Science Lab", 2)],
    "Library":              [("Administration Block", 2)],
    "Science Lab":          [("Administration Block", 2), ("Student Affairs", 2)],
    "Student Affairs":      [("Cafeteria", 2), ("Science Lab", 2)],
    "Cafeteria":            [("Main Gate", 3), ("Student Affairs", 2)],
}


def path_cost(path):
    total = 0
    for here, there in zip(path, path[1:]):
        total += dict(CAMPUS[here])[there]
    return total


def bfs(start, goal, trace=True):
    frontier = deque([[start]])   # queue of whole paths, oldest path first
    seen = {start}                # locations already queued, never queue twice
    expanded = 0

    while frontier:
        if trace:
            print("frontier:", [p[-1] for p in frontier])
        path = frontier.popleft()          # take from the FRONT (oldest)
        node = path[-1]
        expanded += 1
        if trace:
            print("  expand :", node)

        if node == goal:                   # goal test
            return path, path_cost(path), expanded

        for neighbour, _km in CAMPUS[node]:
            if neighbour not in seen:
                seen.add(neighbour)
                frontier.append(path + [neighbour])   # add at the BACK
    return None, None, expanded


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start = args[0] if args else "Main Gate"
    goal = args[1] if len(args) > 1 else "Science Lab"
    if start not in CAMPUS or goal not in CAMPUS:
        sys.exit("Unknown location. Choose from: " + ", ".join(CAMPUS))

    path, cost, expanded = bfs(start, goal, trace="--quiet" not in sys.argv)
    print()
    print("BFS path :", " -> ".join(path))
    print("Cost     :", cost, "km")
    print("Hops     :", len(path) - 1)
    print("Expanded :", expanded)
