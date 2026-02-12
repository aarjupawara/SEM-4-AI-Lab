# River Crossing Problem (3 Girls, 3 Boys)
# Q1: Depth Limited Search (limit = 3)

class RiverCrossingProblem:
    def __init__(self):
        self.initial = (3, 3, 0)   # (Girls_left, Boys_left, Boat_side) all on left
        self.goal = (0, 0, 1)  #all on right

    def goal_test(self, state):
        return state == self.goal

    def is_valid(self, state):
        G_L, B_L, boat = state
        G_R = 3 - G_L
        B_R = 3 - B_L

        if G_L < 0 or B_L < 0 or G_L > 3 or B_L > 3:
            return False

        if G_L > 0 and B_L > G_L:  #on left
            return False 

        if G_R > 0 and B_R > G_R:  #on right
            return False

        return True

    def actions(self, state):
        G_L, B_L, boat = state
        moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]  #(girl, boy)
        valid_moves = []

        for g, b in moves:
            if boat == 0:
                new_state = (G_L - g, B_L - b, 1)
            else:
                new_state = (G_L + g, B_L + b, 0)

            if self.is_valid(new_state):
                valid_moves.append((g, b))

        return valid_moves

    def result(self, state, action):
        G_L, B_L, boat = state
        g, b = action

        if boat == 0:
            return (G_L - g, B_L - b, 1)
        else:
            return (G_L + g, B_L + b, 0)


#Represents a node in search tree.
class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state #Current state
        self.parent = parent
        self.action = action #Action used to reach this node
        self.depth = depth

    #This function generates all child nodes.
    def expand(self, problem):
        children = []  #Empty list to store child nodes.
        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)
            children.append(Node(next_state, self, action, self.depth + 1))
        return children


# ---------------- Depth Limited Search ----------------

def depth_limited_search(problem, limit):
    explored = 0 #Counts visited nodes.

    def recursive_dls(node, limit):
        nonlocal explored
        explored += 1

        if problem.goal_test(node.state):
            return node
        if limit == 0:
            return "cutoff"

        cutoff_occurred = False #remember if any child return cutoff

        #Generate children and explore one by one.
        for child in node.expand(problem):
            result = recursive_dls(child, limit - 1)
            if result == "cutoff":
                cutoff_occurred = True
            elif result is not None: #sol found 
                return result

        return "cutoff" if cutoff_occurred else None #If at least one child hit depth limit → return "cutoff" Else: Return None (dead end).

    root = Node(problem.initial)
    result = recursive_dls(root, limit)
    return result, explored


# ---------------- Main ----------------

if __name__ == "__main__":
    problem = RiverCrossingProblem()
    result, explored = depth_limited_search(problem, 3)

    print("Depth Limited Search (limit = 3)")
    print("States explored:", explored)
    print("Result:", result)


#Time = O(b^L)  b = branching factor L = depth limit
#Space = O(bL)
