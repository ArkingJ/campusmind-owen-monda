# Extension: what changes if MIN moves first

Same game, same 3 plies, same start location (Main Gate), same utility
formula. The only change is that MIN moves first instead of MAX, so the
alternation becomes MIN, then MAX, then MIN.

## Result

- **New game value: -1**
- **MIN's best first move: Main Gate -> Administration Block, value -1**

(Main Gate -> Cafeteria only backs up to 0, so MIN prefers Administration
Block, since -1 is smaller than 0 and MIN always wants the smaller number.)

## Why the value changed

The value did not change because the map or the utility formula changed,
since neither did. It changed because flipping who moves first flips which
player controls each level of backing-up. In the original game, the levels
went MAX, MIN, MAX, so the last full round of choices before the terminal
values were picked belonged to MIN, and the values feeding into the root
belonged to MAX. With MIN moving first, the levels go MIN, MAX, MIN, so it
is now MAX doing the middle-level picking, and it is MIN who both starts
and controls the final backed-up comparison at the root.

Concretely, take the Cafeteria branch. In the original game this branch was
a MIN node choosing between two MAX nodes that had each already picked their
best (largest) option, giving MIN a choice between two 3s, so it stayed 3.
With MIN moving first, Cafeteria is now reached one level earlier and the
node sitting where MIN used to choose is now a MAX node, so it picks the
larger option, Cafeteria (3), while the Administration Block branch is now
a MAX node picking the larger of -1 and 3, again 3, but sitting one level up
means MIN then has to choose between the *first-move* branches themselves,
comparing -1 (Administration Block) against 0 (Cafeteria), and MIN takes the
smaller one. So the swap does not just flip a sign, it changes which level
of the tree gets the "pick the best for me" treatment at each depth, and
that reshuffles which terminal values end up mattering most.
