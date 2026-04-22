from collections import deque

# CSP Class
class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables       #cells
        self.domains = domains           #possible numbers
        self.neighbors = neighbors       #constraints graph
        self.constraint = constraint     #rule function


# Constraint Function
def different_values_constraint(Xi, x, Xj, y):
    return x != y  #Two cells must not have same value



# AC-3
def AC3(csp):
    queue = deque((Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi])

    while queue:
        Xi, Xj = queue.popleft()
        if revise(csp, Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


# REVISE 
def revise(csp, Xi, Xj):
    revised = False

    for x in set(csp.domains[Xi]):
        # remove x if no possible y satisfies constraint
        if not any(csp.constraint(Xi, x, Xj, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True

    return revised


# -----------------------------
# Sudoku Setup
# -----------------------------
grid = [
    [0,0,0,0,0,6,0,0,0],
    [0,5,9,0,0,0,0,0,8],
    [2,0,0,0,0,8,0,0,0],
    [0,4,5,0,0,0,0,0,0],
    [0,0,3,0,0,0,0,0,0],
    [0,0,6,0,0,3,0,5,0],
    [0,0,0,0,0,7,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,2]
]

# Variables
variables = [(r, c) for r in range(9) for c in range(9)]

# Domains
domains = {}
for r, c in variables:
    if grid[r][c] != 0:
        domains[(r, c)] = {grid[r][c]}
    else:
        domains[(r, c)] = set(range(1, 10))


# Neighbors
def get_neighbors(cell):
    r, c = cell
    neighbors = set()

    # Row & Column
    for i in range(9):
        if i != c:
            neighbors.add((r, i))
        if i != r:
            neighbors.add((i, c))

    # 3x3 Box
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if (i, j) != cell:
                neighbors.add((i, j))

    return neighbors


neighbors = {v: get_neighbors(v) for v in variables}

# Create CSP
sudoku = CSP(variables, domains, neighbors, different_values_constraint)

# -----------------------------
# Run AC-3
# -----------------------------
result = AC3(sudoku)

# -----------------------------
# Display Result
# -----------------------------
def print_grid(csp):
    for r in range(9):
        row = []
        for c in range(9):
            if len(csp.domains[(r, c)]) == 1:
                row.append(str(next(iter(csp.domains[(r, c)]))))
            else:
                row.append(".")
        print(" ".join(row))


print("\nSolved (partial by AC-3):\n")
print_grid(sudoku)

print("\nArc Consistent:", result)
print("Solved?", all(len(sudoku.domains[v]) == 1 for v in sudoku.variables))
