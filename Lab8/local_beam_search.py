import random

# -------- Problem Definition --------
class TSPProblem:
    def __init__(self, dist_matrix):
        self.dist = dist_matrix
        self.n = len(dist_matrix)

    def random_state(self):
        return random.sample(range(self.n), self.n)

    def cost(self, state):
        return sum(self.dist[state[i]][state[i+1]] for i in range(self.n-1)) + \
               self.dist[state[-1]][state[0]]

    def value(self, state):
        return -self.cost(state)

    def neighbors(self, state):
        neighbors = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                s = state[:]
                s[i], s[j] = s[j], s[i]
                neighbors.append(s)
        return neighbors


# -------- Helper --------
def format_tour(tour):
    cities = ['A','B','C','D','E','F','G','H']
    path = [cities[i] for i in tour]
    path.append(cities[tour[0]])
    return " → ".join(path)


# -------- Local Beam Search (Randomized) --------
def local_beam_search(problem, k=3, max_iter=100):
    states = [problem.random_state() for _ in range(k)]

    for _ in range(max_iter):
        all_successors = []

        for s in states:
            neighbors = problem.neighbors(s)

            #  Random subset of neighbors
            sampled = random.sample(neighbors, min(10, len(neighbors)))
            all_successors.extend(sampled)

        # Add randomness in selection
        states = sorted(
            all_successors,
            key=lambda s: problem.value(s) + random.uniform(-5, 5),
            reverse=True
        )[:k]

    best = max(states, key=problem.value)
    return best


# -------- Run --------
if __name__ == "__main__":
    dist = [
        [0,10,15,20,25,30,35,40],
        [12,0,35,15,20,25,30,45],
        [25,30,0,10,40,20,15,35],
        [18,25,12,0,15,30,20,10],
        [22,18,28,20,0,15,25,30],
        [35,22,18,28,12,0,40,20],
        [30,35,22,18,28,32,0,15],
        [40,28,35,22,18,25,12,0]
    ]

    problem = TSPProblem(dist)

    for k in [3, 5, 10]:
        result = local_beam_search(problem, k)
        print(f"\nBeam width k={k}")
        print("Path:", format_tour(result))
        print("Cost:", problem.cost(result))
