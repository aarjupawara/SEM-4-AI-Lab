import random

# This function checks whether a cell (x, y) is inside the grid boundaries
#index out-of-range errors.
def is_valid(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


# Randomly place obstacles in the 2D-grid
# 0 -> free cell
# 1 -> obstacle
def place_obstacles(grid, n, m, obstacle_count, start, goal):
    placed = 0

    while placed < obstacle_count:
        x = random.randint(0, n - 1)
        y = random.randint(0, m - 1)

        # Do not place obstacles on start or goal
        if (x, y) != start and (x, y) != goal and grid[x][y] == 0:
            grid[x][y] = 1
            placed += 1


# Dijkstra's Algorithm to construct heuristic table
# Runs from GOAL state
# Heuristic value = shortest distance to goal


#A 2D matrix showing minimum distance to the goal from each cell.
def dijkstra_heuristic(grid, n, m, goal):
    INF = 9999

    heuristic = [[INF for _ in range(m)] for _ in range(n)]
    visited = [[False for _ in range(m)] for _ in range(n)]

    heuristic[goal[0]][goal[1]] = 0

    moves = [(0, 1), (1, 0), (-1, 0), (0, -1)] #Movement directions

    for _ in range(n * m):
        min_dist = INF
        current = None

        for i in range(n):
            for j in range(m):
                if not visited[i][j] and heuristic[i][j] < min_dist:
                    min_dist = heuristic[i][j]
                    current = (i, j)

        if current is None:
            break

        x, y = current
        visited[x][y] = True

        for dx, dy in moves:
            nx = x + dx
            ny = y + dy

            if is_valid(nx, ny, n, m) and grid[nx][ny] != 1:
                if heuristic[nx][ny] > heuristic[x][y] + 1:
                    heuristic[nx][ny] = heuristic[x][y] + 1

    return heuristic


class PriorityQueue:
    def __init__(self, heuristic):
        self.items = []  # Stores (state, path)
        self.heuristic = heuristic

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)


    def pop(self): #Removes and returns the node with the lowest heuristic value
        best_index = 0
        x, y = self.items[0][0]
        best_h = self.heuristic[x][y]

        for i in range(1, len(self.items)):
            x, y = self.items[i][0]
            if self.heuristic[x][y] < best_h:
                best_h = self.heuristic[x][y]
                best_index = i

        return self.items.pop(best_index)


def best_first_search(grid, n, m, start, goal, heuristic):
    frontier = PriorityQueue(heuristic)
    frontier.push((start, [start]))
    visited = set()

    moves = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    while not frontier.is_empty():
        current, path = frontier.pop()

        if current == goal:
            return path

        visited.add(current)

        for dx, dy in moves:
            nx = current[0] + dx
            ny = current[1] + dy
            new_state = (nx, ny)

            if is_valid(nx, ny, n, m):
                if grid[nx][ny] != 1 and new_state not in visited:
                    frontier.push((new_state, path + [new_state]))

    return None



# INPUT SECTION

n = int(input("Enter number of rows (n): "))
m = int(input("Enter number of columns (m): "))

grid = [[0 for _ in range(m)] for _ in range(n)]

obstacles = int(input("Enter number of obstacles: "))

max_obstacles = n * m - 2
if obstacles > max_obstacles:
    print("Too many obstacles! Maximum allowed:", max_obstacles)
    exit()

print("\nNOTE: Enter positions using 1-based indexing")

sx = int(input("Enter start row: ")) - 1
sy = int(input("Enter start column: ")) - 1
gx = int(input("Enter goal row: ")) - 1
gy = int(input("Enter goal column: ")) - 1

if not is_valid(sx, sy, n, m) or not is_valid(gx, gy, n, m):
    print("Invalid start or goal position!")
    exit()

start = (sx, sy)
goal = (gx, gy)


# EXECUTION

place_obstacles(grid, n, m, obstacles, start, goal)

heuristic = dijkstra_heuristic(grid, n, m, goal)

path = best_first_search(grid, n, m, start, goal, heuristic)


print("\nGrid (1 = obstacle):")
for row in grid:
    print(row)

print("\nHeuristic Table (distance to goal):")
for row in heuristic:
    print(row)

print("\nBest-First Search Path:")
print(path)
