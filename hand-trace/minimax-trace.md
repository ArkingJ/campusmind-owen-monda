# Hand trace: the subtree under MAX's move to Cafeteria

This traces, by hand, the branch of the game tree where MAX's first move is
Main Gate to Cafeteria. It stops one move short of the full game, since Part
4 only asks for this one subtree, not the whole tree (the whole tree is
covered by running minimax.py).

Recall the rule: `utility(location) = hop_distance(location, Library) - hop_distance(location, Cafeteria)`

## The subtree

```
MAX moves: Main Gate -> Cafeteria           (this is the branch being traced)

  MIN to move at Cafeteria. MIN's options: Main Gate, Student Affairs

    MIN option 1: Cafeteria -> Main Gate
      MAX to move at Main Gate. MAX's options: Administration Block, Cafeteria

        MAX option 1: Main Gate -> Administration Block   [terminal, 3 moves made]
          utility(Administration Block) = 1 - 2 = -1

        MAX option 2: Main Gate -> Cafeteria               [terminal, 3 moves made]
          utility(Cafeteria) = 3 - 0 = 3

      MAX picks the larger of its two options: max(-1, 3) = 3
      Backed-up value at Main Gate (MAX node) = 3

    MIN option 2: Cafeteria -> Student Affairs
      MAX to move at Student Affairs. MAX's options: Cafeteria, Science Lab

        MAX option 1: Student Affairs -> Cafeteria         [terminal, 3 moves made]
          utility(Cafeteria) = 3 - 0 = 3

        MAX option 2: Student Affairs -> Science Lab       [terminal, 3 moves made]
          utility(Science Lab) = 2 - 2 = 0

      MAX picks the larger of its two options: max(3, 0) = 3
      Backed-up value at Student Affairs (MAX node) = 3

  MIN picks the smaller of its two options: min(3, 3) = 3
  Backed-up value at Cafeteria (MIN node) = 3
```

## Summary table

| Node (who moves next) | Options tried | Terminal utilities | Backed-up value |
|---|---|---|---|
| Main Gate (MAX, after MIN went here) | Admin Block, Cafeteria | -1, 3 | max = 3 |
| Student Affairs (MAX, after MIN went here) | Cafeteria, Science Lab | 3, 0 | max = 3 |
| Cafeteria (MIN, after MAX's first move) | Main Gate, Student Affairs | 3, 3 | min = 3 |

So the value of MAX's first move to Cafeteria is **3**. This is the number
`minimax.py` prints as `Main Gate -> Cafeteria: 3`, and it is the value that
ends up winning at the root, since the other first move (to Administration
Block) only backs up to -1.
