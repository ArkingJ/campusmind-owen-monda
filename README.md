Name: Owen Monda
Registration Number: SCT-253-013/2023
# CampusMind

A small program that finds routes around a campus with six locations. I built it for ICS 2413 Artificial Intelligence using plain Python 3 so there is nothing to install.

## How to run

```
python bfs/bfs.py
python dfs/dfs.py
python dfs/dfs.py --reverse
python astar/astar.py
```

Each script shows what is in the frontier and which location gets expanded at every step and then prints the final path with its cost. To try another route put two location names in quotes after the script name. Add --quiet to hide the steps.

## Part 2 BFS and DFS

I tested both on Main Gate to Science Lab.

**Which path did each find**

Both found Main Gate then Administration Block then Science Lab which costs 3 km. BFS expanded 5 locations and DFS expanded 4.

**Were the paths different**

Not this time but only because of the order the map lists the neighbours. DFS tries the first listed neighbour first and Administration Block comes before Cafeteria. With --reverse DFS goes to the Cafeteria first and ends up on Main Gate then Cafeteria then Student Affairs then Science Lab which costs 7 km. BFS gives the same answer either way because it works through the map one layer at a time.

**Which would I prefer**

BFS when I want the fewest connections and do not want the answer to depend on how the map is written. It ignores kilometres though so it cannot be trusted to find the cheapest route on every map. DFS is fine when any route will do or memory is short but it can hand back a long route without any warning.

## Part 3 A*

The code is in the astar folder. The full comparison of BFS and DFS and A* is in search-comparison/03-search-comparison.pdf