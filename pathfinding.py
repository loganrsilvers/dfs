from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]

MODE = "BFS"  # Change to "DFS" for a goofier monster.

EXAMPLE_MAP_1 = """
##########
#S..#....#
#.#.#.##.#
#.#...#.G#
##########
""".strip("\n")

EXAMPLE_MAP_2 = """
############
#S....#....#
#.##.#.##..#
#....#..#G.#
#.######.#.#
#..........#
############
""".strip("\n")

CHASE_MAP = """
############
#P..#......#
#.#.#.####.#
#.#...#..G.#
#.###.#.##.#
#...#...M..#
############
""".strip("\n")


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    rows = [list(line) for line in text.splitlines() if line.strip()]
    if not rows:
        raise ValueError("Grid cannot be empty")

    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("Grid must be rectangular")

    start: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "S":
                if start is not None:
                    raise ValueError("Grid must contain exactly one S")
                start = (r, c)
            elif ch == "G":
                if goal is not None:
                    raise ValueError("Grid must contain exactly one G")
                goal = (r, c)
            elif ch not in {"#", ".", "S", "G"}:
                raise ValueError(f"Unexpected tile: {ch!r}")

    if start is None or goal is None:
        raise ValueError("Grid must contain one S and one G")

    return rows, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    r, c = node
    out: List[Pos] = []
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            out.append((nr, nc))

    return out


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if start == goal:
        return [start]
    if goal not in parent:
        return None

    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    q = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while q:
        cur = q.popleft()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt in visited:
                continue
            visited.add(nxt)  # Mark visited when enqueued.
            parent[nxt] = cur
            q.append(nxt)

    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        cur = stack.pop()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt in visited:
                continue
            visited.add(nxt)  # Mark visited when pushed.
            parent[nxt] = cur
            stack.append(nxt)

    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules:
    - path tiles shown as '*'
    - visited tiles shown as '+'
    - preserve 'S' and 'G'
    """
    canvas = [row[:] for row in grid]
    path_set = set(path or [])
    visited_set = visited or set()

    for r in range(len(canvas)):
        for c in range(len(canvas[0])):
            if canvas[r][c] in {"S", "G", "#"}:
                continue
            pos = (r, c)
            if pos in path_set:
                canvas[r][c] = "*"
            elif pos in visited_set:
                canvas[r][c] = "+"

    return "\n".join("".join(row) for row in canvas)


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

    print("=" * 60)
    print(label)
    print("- Raw map")
    print(render(grid))

    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    print("\n- BFS")
    print(f"found={path_bfs is not None} path_len={(len(path_bfs) if path_bfs else None)} visited={len(visited_bfs)}")
    print(render(grid, path=path_bfs, visited=visited_bfs))

    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    print("\n- DFS")
    print(f"found={path_dfs is not None} path_len={(len(path_dfs) if path_dfs else None)} visited={len(visited_dfs)}")
    print(render(grid, path=path_dfs, visited=visited_dfs))


def _find_char(grid: Grid, target: str) -> Pos:
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == target:
                return (r, c)
    raise ValueError(f"Tile {target!r} not found")


def _parse_chase_grid(text: str) -> Tuple[Grid, Pos, Pos, Optional[Pos]]:
    rows = [list(line) for line in text.splitlines() if line.strip()]
    player = _find_char(rows, "P")
    monster = _find_char(rows, "M")
    goal: Optional[Pos] = None
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "G":
                goal = (r, c)
            if ch in {"P", "M", "G"}:
                continue
            if ch not in {"#", "."}:
                raise ValueError(f"Unexpected chase tile: {ch!r}")
    return rows, player, monster, goal


def _path_for_mode(grid: Grid, start: Pos, goal: Pos) -> Optional[List[Pos]]:
    temp = [row[:] for row in grid]
    temp[start[0]][start[1]] = "S"
    temp[goal[0]][goal[1]] = "G"
    if MODE.upper() == "BFS":
        path, _ = bfs_path(temp, start, goal)
        return path
    path, _ = dfs_path(temp, start, goal)
    return path


def game_loop() -> None:
    """Simple turn-based Monster Chase console mini-game."""
    grid, player, monster, goal = _parse_chase_grid(CHASE_MAP)

    print("\n" + "=" * 60)
    print(f"Monster Chase (MODE={MODE.upper()})")
    print("Use WASD then Enter. q quits.")

    deltas = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}

    while True:
        view = [row[:] for row in grid]
        view[player[0]][player[1]] = "P"
        view[monster[0]][monster[1]] = "M"
        print(render(view))

        if player == monster:
            print("The monster caught you. You lose.")
            return
        if goal is not None and player == goal:
            print("You reached the exit. You win!")
            return

        cmd = input("Move (W/A/S/D or q): ").strip().lower()
        if cmd == "q":
            print("Quit game.")
            return
        if cmd not in deltas:
            print("Invalid move.")
            continue

        dr, dc = deltas[cmd]
        pr, pc = player[0] + dr, player[1] + dc
        if not (0 <= pr < len(grid) and 0 <= pc < len(grid[0])) or grid[pr][pc] == "#":
            print("Bumped into a wall.")
            continue
        player = (pr, pc)

        chase_path = _path_for_mode(grid, monster, player)
        if chase_path and len(chase_path) > 1:
            monster = chase_path[1]


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)


if __name__ == "__main__":
    main()
