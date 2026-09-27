"""The CampusMind Challenge game.

One token starts at the Main Gate. MAX and MIN alternate turns moving the
token along the campus map (movement works in both directions, exactly as
in Weeks 1 to 3). MAX moves first. The game lasts 3 plies (3 moves total,
so the sequence is MAX, MIN, MAX).

After the 3rd move, the location the token ends up at is scored with:

    utility(location) = hop_distance(location, Library) - hop_distance(location, Cafeteria)

hop_distance counts connections (hops), not kilometres, so it is the same
kind of count used for the hop-count heuristic in Week 3.
"""
from collections import deque

# Neighbour order matters for Part 3 (alpha-beta pruning), so this list is
# written in the same order the campus map was given in Weeks 1-3.
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


def hop_distance(start, goal):
    """Fewest connections between start and goal, ignoring distance in km."""
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


if __name__ == "__main__":
    print("Utility of every location (used to score the game once 3 moves are made):")
    for place in CAMPUS:
        print(f"  {place:22s} hops to Library = {hop_distance(place, 'Library')}, "
              f"hops to Cafeteria = {hop_distance(place, 'Cafeteria')}, "
              f"utility = {utility(place)}")
