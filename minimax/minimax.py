"""Minimax search for the CampusMind Challenge game.

Run:  python3 minimax.py
Add --quiet to hide the per-move trace.
"""
import sys
from collections import deque

# Same map and utility as game/campusmind_challenge.py. Kept self-contained
# here (same approach as bfs.py, dfs.py, astar.py in Weeks 1-3) so this file
# runs on its own with no import path to set up.
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


leaf_count = 0  # how many terminal states minimax actually looked at


def minimax(location, depth, maximizing):
    """Return the game value from `location` with `depth` moves already made.

    maximizing=True means it is MAX's turn to move next from this location.
    """
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
        print(f"{indent}{turn} to move at {location} (depth {depth})")

    if maximizing:
        best = float("-inf")
        for neighbour in CAMPUS[location]:
            value = minimax(neighbour, depth + 1, False)
            best = max(best, value)
        return best
    else:
        best = float("inf")
        for neighbour in CAMPUS[location]:
            value = minimax(neighbour, depth + 1, True)
            best = min(best, value)
        return best


if __name__ == "__main__":
    print(f"Minimax on the CampusMind Challenge game, starting at {START}")
    print(f"{TOTAL_PLIES} plies total, MAX moves first")
    print()

    root_children = {}
    for neighbour in CAMPUS[START]:
        if TRACE:
            print(f"--- MAX's option: {START} -> {neighbour} ---")
        value = minimax(neighbour, 1, False)   # 1 move made, MIN to move next
        root_children[neighbour] = value
        if TRACE:
            print()

    print("MAX's first-move options:")
    for place, value in root_children.items():
        print(f"  {START} -> {place}: {value}")

    game_value = max(root_children.values())
    print()
    print("Full game value from", START, "=", game_value)
    print("Terminal states evaluated:", leaf_count)
