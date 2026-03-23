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
        return -self.cost(state)   # AIMA style


# -------- Convert Tour to City Names --------
def format_tour(tour):
    cities = ['A','B','C','D','E','F','G','H']
    path = [cities[i] for i in tour]
    path.append(cities[tour[0]])
    return " → ".join(path)


# -------- Selection (FIXED) --------
def weighted_selection(population, problem):
    costs = [problem.cost(ind) for ind in population]
    max_cost = max(costs)

    # Convert to positive fitness
    weights = [max_cost - c + 1 for c in costs]

    total = sum(weights)
    pick = random.uniform(0, total)

    current = 0
    for ind, w in zip(population, weights):
        current += w
        if current >= pick:
            return ind

    return population[-1]  # safety fallback


# -------- Crossover Operators --------
def crossover_one_point(p1, p2):
    n = len(p1)
    c = random.randint(1, n-2)
    child = p1[:c] + [x for x in p2 if x not in p1[:c]]
    return child


def crossover_two_point(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))

    middle = p1[a:b]
    rest = [x for x in p2 if x not in middle]

    return rest[:a] + middle + rest[a:]


# -------- Mutation --------
def mutate(individual, rate=0.1):
    if random.random() < rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual


# -------- Genetic Algorithm --------
def genetic_algorithm(problem, pop_size=50, generations=200, crossover="one"):
    population = [problem.random_state() for _ in range(pop_size)]

    for _ in range(generations):
        new_population = []

        # -------- Elitism (keep best) --------
        best = min(population, key=problem.cost)
        new_population.append(best)

        while len(new_population) < pop_size:
            p1 = weighted_selection(population, problem)
            p2 = weighted_selection(population, problem)

            if crossover == "one":
                child = crossover_one_point(p1, p2)
            else:
                child = crossover_two_point(p1, p2)

            child = mutate(child)
            new_population.append(child)

        population = new_population

    best = min(population, key=problem.cost)
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

    print("\n--- Genetic Algorithm (1-point crossover) ---")
    res1 = genetic_algorithm(problem, crossover="one")
    print("Path:", format_tour(res1))
    print("Cost:", problem.cost(res1))

    print("\n--- Genetic Algorithm (2-point crossover) ---")
    res2 = genetic_algorithm(problem, crossover="two")
    print("Path:", format_tour(res2))
    print("Cost:", problem.cost(res2))
