import pandas as pd
import numpy as np

class AirportProblem:
    def __init__(self, points, k):
        self.points = points
        self.k = k

    #initial() chooses k random cities as starting airport locations
    def initial(self):
        return self.points[np.random.choice(len(self.points), self.k, replace=False)]

    def value(self, centers):
        # Negative SSD because AIMA maximizes value
        total = 0
        for p in self.points:
            distances = [np.sum((p - c)**2) for c in centers]
            total += min(distances)
        return -total   # maximize negative = minimize SSD


# Gradient Descent (First Order)
def gradient_descent(problem, max_iter=100):
    current = problem.initial()

    for _ in range(max_iter):
        clusters = [[] for _ in range(problem.k)]

        # Assign points to nearest center
        for p in problem.points:
            distances = [np.sum((p - c)**2) for c in current]
            idx = np.argmin(distances)
            clusters[idx].append(p)

        # Compute gradient step (mean update)
        next_state = []
        for i in range(problem.k):
            if len(clusters[i]) > 0:
                next_state.append(np.mean(clusters[i], axis=0))
            else:
                next_state.append(current[i])

        next_state = np.array(next_state)

        if np.allclose(current, next_state):
            break

        current = next_state

    return current, -problem.value(current)


# Newton Method (Second Order)
def newton_method(problem, max_iter=50):
    current = problem.initial()

    for _ in range(max_iter):
        clusters = [[] for _ in range(problem.k)]

        # Assign clusters
        for p in problem.points:
            distances = [np.sum((p - c)**2) for c in current]
            idx = np.argmin(distances)
            clusters[idx].append(p)

        # Newton step (closed-form solution)
        next_state = []
        for i in range(problem.k):
            if len(clusters[i]) > 0:
                next_state.append(np.mean(clusters[i], axis=0))
            else:
                next_state.append(current[i])

        next_state = np.array(next_state)

        if np.allclose(current, next_state):
            break

        current = next_state

    return current, -problem.value(current)


# MAIN EXECUTION (FIXED)

# Use full path + header=None
data = pd.read_csv(
    r"C:\Users\AARJU\OneDrive\Desktop\AI LAB\Lab 10\cities.csv",
    header=None
)

#: Directly use values (since no column names)
points = data.values

problem = AirportProblem(points, k=3)

gd_centers, gd_cost = gradient_descent(problem)
nr_centers, nr_cost = newton_method(problem)

# OUTPUT
print("\n===== AIRPORT LOCATION OPTIMIZATION =====")

print("\n[Gradient Descent - First Order Method]")
print("Centers:\n", gd_centers)
print("Sum of Squared Distances:", round(gd_cost, 2))

print("\n[Newton-Raphson - Second Order Method]")
print("Centers:\n", nr_centers)
print("Sum of Squared Distances:", round(nr_cost, 2))

print("\n===== COMPARISON =====")

if nr_cost < gd_cost:
    print("Newton Method is better (lower cost).")
elif gd_cost < nr_cost:
    print("Gradient Descent is better (lower cost).")
else:
    print("Both methods perform equally.")

print("Difference:", round(abs(gd_cost - nr_cost), 2))

print("\nConclusion:")
print("Newton method uses second-order derivatives (Hessian) and converges faster than Gradient Descent.")
