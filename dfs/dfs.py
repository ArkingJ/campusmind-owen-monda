"""Depth-first search on the CampusMind map.

Run:  python3 dfs.py                      (Main Gate to Science Lab)
      python3 dfs.py --reverse            (try neighbours in the opposite order)
      python3 dfs.py "Library" "Cafeteria"
Add --quiet to hide the step-by-step trace.
"""
import sys

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


def dfs(start, goal, reverse=False, trace=True):
    stack = [[start]]     # stack of whole paths, newest path last
    visited = set()       # locations already expanded
    expanded = 0

    while stack:
        if trace:
            print("stack   :", [p[-1] for p in stack], "(top is the right end)")
        path = stack.pop()                 # take from the END (newest)
        node = path[-1]
        if node in visited:                # stale copy, we already went here
            continue
        visited.add(node)
        expanded += 1
        if trace:
            print("  expand:", node)

        if node == goal:                   # goal test
            return path, path_cost(path), expanded

        neighbours = [n for n, _km in CAMPUS[node] if n not in visited]
        # A stack pops the last thing pushed, so push in reverse to make the
        # first-listed neighbour the one we try first. --reverse flips this.
        order = neighbours if reverse else list(reversed(neighbours))
        for neighbour in order:
            stack.append(path + [neighbour])
    return None, None, expanded


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start = args[0] if args else "Main Gate"
    goal = args[1] if len(args) > 1 else "Science Lab"
    if start not in CAMPUS or goal not in CAMPUS:
        sys.exit("Unknown location. Choose from: " + ", ".join(CAMPUS))

    path, cost, expanded = dfs(start, goal, reverse="--reverse" in sys.argv,
                               trace="--quiet" not in sys.argv)
    print()
    print("DFS path :", " -> ".join(path))
    print("Cost     :", cost, "km")
    print("Hops     :", len(path) - 1)
    print("Expanded :", expanded)
