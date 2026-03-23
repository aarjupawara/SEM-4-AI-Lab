import random
import math

# Q2: Variants of Hill Climbing

N = 8
# state = (0, 4, 7, 5, 2, 6, 1, 3)  index=col and values=rows.

# Heuristic Function
def heuristic(state):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            # Same row OR same diagonal → conflict |row difference| == |column difference|
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Generate random neighbor (used in first-choice & Simulated Annealing)
def random_neighbor(state):
    col = random.randint(0, N - 1)
    row = random.randint(0, N - 1)
    new_state = list(state)
    new_state[col] = row
    return tuple(new_state)


# First-Choice Hill Climbing
# Picks first better neighbor found 
#Instead of checking all neighbors, it:Randomly generates neighbors ,Accepts the first better one, Stops when no improvement found
def first_choice(initial_state):
    current = initial_state
    steps = 0

    while True:
        current_h = heuristic(current)
        improved = False

        # Try random moves until improvement found
        for _ in range(100):
            neighbor = random_neighbor(current)
            if heuristic(neighbor) < current_h:
                current = neighbor
                steps += 1
                improved = True
                break

        if not improved:
            return current, heuristic(current), steps
        
#imitation : Gets stuck in local minima, Cannot escape plateaus


# Steepest-Ascent (for random restart)
#Look at all possible neighbors and pick the best one.
def steepest_ascent(state):
    current = state
    steps = 0

    while True:
        current_h = heuristic(current)
        neighbors = []

        #For each column: Try moving queen to every other row. Total neighbors: 56
        for col in range(N):
            for row in range(N):
                if row != current[col]:
                    new_state = list(current)
                    new_state[col] = row
                    neighbors.append(tuple(new_state))

        best_neighbor = min(neighbors, key=heuristic)
        best_h = heuristic(best_neighbor)

        if best_h >= current_h:
            return current, current_h, steps

        current = best_neighbor
        steps += 1


# Random Restart Hill Climbing. If stuck in local minimum: Restart from a new random board
# Restart until solution found 
#complete algo    O(R · S · N⁴)
def random_restart(max_restarts=100):
    total_steps = 0

    for restart in range(max_restarts):
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        final_state, final_h, steps = steepest_ascent(initial_state)

        total_steps += steps

        if final_h == 0:
            return final_state, final_h, total_steps, restart + 1

    return final_state, final_h, total_steps, max_restarts


# Simulated Annealing  O(T · N²)

# Allows occasional uphill moves
# metal cooling process. High temperature: more exploration. Low temperature: greedy behavior
def simulated_annealing(initial_state):
    current = initial_state

    for t in range(10000):

        T = max(0.01, 1 - t * 0.001)  # Cooling schedule

        if T <= 0:
            break

        neighbor = random_neighbor(current)

        delta = heuristic(current) - heuristic(neighbor)

        # Accept better OR sometimes worse (probabilistically)
        if delta > 0 or random.random() < math.exp(delta / T):
            current = neighbor

        if heuristic(current) == 0:
            return current, 0

    return current, heuristic(current)



print("\n Comparison of Hill Climbing Variants\n")

algorithms = ["First Choice","Steepest Ascent", "Random Restart", "Simulated Annealing"]

for algo in algorithms:

    success = 0

    for _ in range(50):

        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))

        if algo == "First Choice":
            _, h, _ = first_choice(initial_state)

        elif algo == "Steepest Ascent":
            _, h, _ = steepest_ascent(initial_state)

        elif algo == "Random Restart":
            _, h, _, _ = random_restart()

        elif algo == "Simulated Annealing":
            _, h = simulated_annealing(initial_state)

        if h == 0:
            success += 1

    print(f"{algo:20s} → Success Rate = {success}/50")
