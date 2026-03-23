import heapq

graph = {
    "Syracuse": {"Buffalo":150, "Boston":312, "New York":254, "Philadelphia":253},
    "Buffalo": {"Syracuse":150, "Detroit":256, "Cleveland":189, "Pittsburgh":215},
    "Detroit": {"Buffalo":256, "Chicago":283, "Cleveland":169},
    "Chicago": {"Detroit":283, "Cleveland":345, "Indianapolis":182},
    "Cleveland": {"Chicago":345, "Buffalo":189, "Pittsburgh":134, "Detroit":283, "Columbus":144},
    "Pittsburgh": {"Cleveland":134, "Philadelphia":305, "Buffalo":215, "Columbus":185, "Baltimore":247},
    "Philadelphia": {"Pittsburgh":305, "New York":97, "Baltimore":101},
    "New York": {"Philadelphia":97, "Boston":215, "Providence":181, "Syracuse":254},
    "Boston": {"New York":215, "Portland":107, "Providence":50, "Syracuse":312},
    "Indianapolis": {"Chicago":182, "Columbus":176},
    "Columbus": {"Indianapolis":176, "Pittsburgh":185, "Cleveland":144},
    "Providence": {"Boston":50, "New York":181},
    "Portland": {"Boston":107}
}

# Heuristic values h(n) to Boston
h = {
    "Boston": 0,
    "Providence": 50,
    "Portland": 107,
    "New York": 215,
    "Philadelphia": 270,
    "Baltimore": 360,
    "Syracuse": 260,
    "Buffalo": 400,
    "Pittsburgh": 470,
    "Cleveland": 550,
    "Columbus": 640,
    "Detroit": 610,
    "Indianapolis": 780,
    "Chicago": 860
}

# Node class 
# each node stores: curent city, parent node, total path cost
class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def expand(self):
        children = []
        for neighbor, cost in graph[self.state].items():
            child = Node(neighbor, self, self.path_cost + cost)
            children.append(child)
        return children

    def solution(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))


# Best First Graph Search  
def best_first_graph_search(start, goal, f):
    node = Node(start)
    frontier = []
    counter = 0   # tie-breaker

    heapq.heappush(frontier, (f(node), counter, node))
    explored = set()
    explored_count = 0

    while frontier:
        _, _, current = heapq.heappop(frontier) #Removes node with smallest f(n).
        explored_count += 1

        if current.state == goal:
            return current.solution(), explored_count

        explored.add(current.state)
        
        #If city not visited: Increase counter Add to frontier Priority based on f(n)
        for child in current.expand():
            if child.state not in explored:
                counter += 1
                heapq.heappush(frontier, (f(child), counter, child))

    return None, explored_count


# Greedy Best First Search  f(n) = h(n)
def greedy_search(start, goal):
    return best_first_graph_search(start, goal,
                                   lambda n: h[n.state])


# A* Search  f(n) = g(n) + h(n)
def astar_search(start, goal):
    return best_first_graph_search(start, goal,
                                   lambda n: n.path_cost + h[n.state])


#run
start = "Chicago"
goal = "Boston"

greedy_path, greedy_explored = greedy_search(start, goal)
astar_path, astar_explored = astar_search(start, goal)

print("Greedy Path:", greedy_path)
print("Greedy Cities Explored:", greedy_explored)

print("\nA* Path:", astar_path)
print("A* Cities Explored:", astar_explored)
