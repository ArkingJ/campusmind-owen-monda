"""Alpha-beta pruning for the CampusMind Challenge game.

Run:  python3 alphabeta.py
Add --quiet to hide the per-move trace, including which branches get pruned.
"""
import sys
from collections import deque

CAMPUS = {
    "Main Gate":            ["Administration Block", "Cafeteria"],
    "Administration Block": ["Main Gate", "Library", "Science Lab"],
    "Library":              ["Administration Block"],
    "Science Lab":          ["Administration Block", "Student Affairs"],
    "Student Affairs":      ["Cafeteria", "Science Lab"],
    "Cafeteria":            ["Main Gate", "Student Affairs"],
}
START = "Main Gate"
TOTAL_PLIES = 3
TRACE = "--quiet" not in sys.argv


def hop_distance(start, goal):
    if start == goal:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for neighbour in CAMPUS[node]:
            if neighbour == goal:
                return dist + 1
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, dist + 1))
    raise ValueError(f"{goal} is not reachable from {start}")


def utility(location):
    return hop_distance(location, "Library") - hop_distance(location, "Cafeteria")


leaf_count = 0  # how many terminal states alpha-beta actually looked at


def alphabeta(location, depth, alpha, beta, maximizing):
    global leaf_count
    indent = "  " * depth

    if depth == TOTAL_PLIES:
        leaf_count += 1
        value = utility(location)
        if TRACE:
            print(f"{indent}terminal at {location}: utility = {value}")
        return value

    turn = "MAX" if maximizing else "MIN"
    if TRACE:
        print(f"{indent}{turn} to move at {location} (depth {depth}, "
              f"alpha={alpha}, beta={beta})")

    if maximizing:
        value = float("-inf")
        for neighbour in CAMPUS[location]:
            value = max(value, alphabeta(neighbour, depth + 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                if TRACE:
                    remaining = CAMPUS[location][CAMPUS[location].index(neighbour) + 1:]
                    print(f"{indent}beta cut-off at {location}: alpha={alpha} >= "
                          f"beta={beta}, skipping {remaining}")
                break
        return value
    else:
        value = float("inf")
        for neighbour in CAMPUS[location]:
            value = min(value, alphabeta(neighbour, depth + 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                if TRACE:
                    remaining = CAMPUS[location][CAMPUS[location].index(neighbour) + 1:]
                    print(f"{indent}alpha cut-off at {location}: alpha={alpha} >= "
                          f"beta={beta}, skipping {remaining}")
                break
        return value


if __name__ == "__main__":
    print(f"Alpha-beta on the CampusMind Challenge game, starting at {START}")
    print(f"{TOTAL_PLIES} plies total, MAX moves first")
    print()

    # This loop is exactly what a single call alphabeta(START, 0, -inf, inf, True)
    # would do inside its own maximizing branch. Writing it out here lets us
    # print each of MAX's first-move options while still carrying alpha
    # forward from one branch into the next, which is what makes the second
    # branch's pruning possible.
    alpha, beta = float("-inf"), float("inf")
    root_children = {}
    game_value = float("-inf")
    for neighbour in CAMPUS[START]:
        if TRACE:
            print(f"--- MAX's option: {START} -> {neighbour} (alpha={alpha}, beta={beta}) ---")
        value = alphabeta(neighbour, 1, alpha, beta, False)
        root_children[neighbour] = value
        game_value = max(game_value, value)
        alpha = max(alpha, game_value)
        if TRACE:
            print()

    print("MAX's first-move options:")
    for place, value in root_children.items():
        print(f"  {START} -> {place}: {value}")

    print()
    print("Full game value from", START, "=", game_value)
    print("Terminal states evaluated:", leaf_count)
