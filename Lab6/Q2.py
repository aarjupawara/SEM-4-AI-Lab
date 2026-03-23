import heapq

# Maze Representation
maze = [
    [2, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
]

ROWS, COLS = 5, 5

# Find start and rewards
rewards = set()
for i in range(ROWS):
    for j in range(COLS):
        if maze[i][j] == 2:
            start = (i, j)
        if maze[i][j] == 3:
            rewards.add((i, j))

# Manhattan Heuristic
def heuristic(pos, remaining_rewards):
    return min(abs(pos[0] - r[0]) + abs(pos[1] - r[1])
               for r in remaining_rewards)

# Valid moves
def neighbors(pos):
    x, y = pos
    moves = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] != 1:
            moves.append((nx, ny))
    return moves

# A* Search to collect all rewards
def astar_collect_all(start, rewards):
    frontier = []
    heapq.heappush(frontier, (0, start, frozenset(rewards), [start]))
    visited = set()

    while frontier:
        f, current, remaining, path = heapq.heappop(frontier)

        state = (current, remaining)
        if state in visited:
            continue
        visited.add(state)

        # Reward collected
        if current in remaining:
            remaining = remaining - {current}

        # All rewards collected
        if not remaining:
            return path

        for nxt in neighbors(current):
            g = len(path)
            h = heuristic(nxt, remaining)
            heapq.heappush(frontier,
                (g + h, nxt, remaining, path + [nxt]))

    return None


path = astar_collect_all(start, rewards)

print("Tiles visited in order:")
for step in path:
    print(step)
print("\nTotal tiles visited:", len(path))
