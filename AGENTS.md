# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (Python list, iterative)
- Parent-map path reconstruction

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`).
- Do not change function signatures in `pathfinding.py`.
- DFS must be iterative (no recursion).
- BFS must use `collections.deque`.
- Use `visited` set and `parent` dict for path reconstruction.
- Mark nodes visited when they are enqueued/pushed.
- Keep changes minimal and keep `main()` runnable.

## Output Contract
Running `python pathfinding.py` must:
- run BFS and DFS on at least 2 maps
- print found/path length/visited count
- print a rendered map with overlays

## Student Guidance
- Put all repo rules in this file so Codex follows them.
- If Codex goes off-track, paste failing output and say: "follow AGENTS.md; minimal diff; fix only X".
