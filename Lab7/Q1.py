import random

# Q1: Steepest-Ascent Hill Climbing for 8-Queens

N = 8  # Board size
# state = (0, 4, 7, 5, 2, 6, 1, 3)  index=col and values=rows.

# Heuristic Function
# h(n) = number of attacking queen pairs 28 pairs.
# Goal state has h(n) = 0

def heuristic(state):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            # Same row OR same diagonal → conflict |row difference| == |column difference|
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts 

# Generate all neighboring states 8*7=56
# Move one queen in its column to another row
def get_neighbors(state):
    neighbors = []
    for col in range(N):
        for row in range(N):
            if row != state[col]:
                new_state = list(state)
                new_state[col] = row
                neighbors.append(tuple(new_state))
    return neighbors

# Steepest-Ascent Hill Climbing
# Always choose best neighbor (minimum heuristic) . Stops if no improvement → Local minimum
#Generate all neighbors and Choose the one with lowest heuristic
def steepest_ascent(initial_state):
    current = initial_state
    steps = 0

    while True:
        current_h = heuristic(current)
        neighbors = get_neighbors(current)

        # Find neighbor with minimum heuristic value
        best_neighbor = min(neighbors, key=heuristic)
        best_h = heuristic(best_neighbor)

        # If no better neighbor exists → STOP (local minimum)
        if best_h >= current_h:
            return current, current_h, steps

        # Move to better state
        current = best_neighbor
        steps += 1

#A local minimum is: A state where no neighbor is better, but it's NOT the solution.


# Run Experiment 50 Times

print("\nQ1: Steepest-Ascent Hill Climbing (50 Runs)\n")

local_minima_found = False

for run in range(1, 51):

    # Generate random board (one queen per column)
    initial_state = tuple(random.randint(0, N - 1) for _ in range(N))

    initial_h = heuristic(initial_state)

    final_state, final_h, steps = steepest_ascent(initial_state)

    status = "Solved" if final_h == 0 else "Fail"

    # Proving Local Minimum:
    # If final_h > 0 and no better neighbor exists → Local minimum
    if status == "Fail":
        local_minima_found = True

    print(f"Run {run:2d}: Initial h = {initial_h:2d}, "
          f"Final h = {final_h:2d}, "
          f"Steps = {steps:2d}, "
          f"Status = {status}")

# Show proof of local minima
if local_minima_found:
    print("\nLocal minimum detected (algorithm stopped with h > 0).")

#O(N2)×O(N2)=O(N4)
