# BFS + DFS Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

The script runs BFS and DFS on two built-in maps and prints:
- whether a path was found
- path length
- number of visited nodes
- rendered overlays (`*` for path and `+` for visited)

## What to look for
- **BFS** explores layer-by-layer and guarantees a shortest path in this unweighted 4-neighbor grid.
- **DFS** explores deep along one branch first, so it may still find a path, but often a longer one.

## Reflection (Assignment Write-up)
### Example where DFS is longer than BFS
On the included examples, DFS can take a branch that heads away from `G` before eventually turning back. Because this code uses a stack and marks visited on push, DFS commits to the latest discovered branch and can discover `G` on a longer route than BFS. BFS, by contrast, discovers nodes by increasing distance from `S`, so the first time `G` is reached is the shortest route in number of steps.

### Compare visited counts
Visited counts vary by map and neighbor order. In narrow corridors, DFS may visit fewer nodes if it gets lucky and runs straight toward the goal. On branchy maps, DFS can also visit many irrelevant nodes before finding `G`, while BFS may spread broadly but still reaches the goal with a minimal path. The printed `visited=` metric in each run makes this comparison concrete.

### Why BFS guarantees shortest path here, but DFS does not
This grid is an **unweighted graph**: each move (up/down/left/right) has equal cost (1). BFS processes nodes in distance layers: first all nodes 1 move away, then 2, then 3, etc. Therefore, when BFS first reaches `G`, no shorter undiscovered path can exist. DFS does not maintain distance layers. It follows one branch to depth before checking alternatives, so the first found goal may be longer than another path that DFS has not explored yet.

## Simple game idea: Monster Chase (Turn-Based)
`pathfinding.py` also includes an optional `game_loop()` implementation with:
- `P` player
- `M` monster
- `#` walls
- `.` floor
- `G` optional exit

Rules:
- Player moves using WASD.
- Monster recomputes a path to the player each turn.
- Monster algorithm is chosen by `MODE = "BFS"` or `MODE = "DFS"`.
- Monster moves one step along that computed path each turn.
- If monster reaches player: lose. If player reaches `G`: win.

> To play, open `pathfinding.py` and call `game_loop()` manually (for example, from a Python REPL).
