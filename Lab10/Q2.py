
class VacuumProblem:
    def __init__(self, initial):
        self.initial = initial #(location, status of A, status of B)

    def ACTIONS(self, state):
        return ['Suck', 'Left', 'Right']

    def RESULT(self, state, action):
        # Non-deterministic outcomes (returns list of states)
        (loc, A, B) = state
        results = []

        if action == 'Suck':
            if loc == 'A':
                # Clean A, maybe clean B also
                results.append(('A', 'Clean', B))
                results.append(('A', 'Clean', 'Clean'))
            else:
                results.append(('B', A, 'Clean'))
                results.append(('B', 'Clean', 'Clean'))

        elif action == 'Left': #vacuum moves to A.
            results.append(('A', A, B))

        elif action == 'Right': #vacuum moves to B.
            results.append(('B', A, B))

        return results

    def GOAL_TEST(self, state):
        (_, A, B) = state
        return A == 'Clean' and B == 'Clean'


# AND-OR-GRAPH-SEARCH (AIMA)
def AND_OR_GRAPH_SEARCH(problem):
    return OR_SEARCH(problem.initial, problem, [])


def OR_SEARCH(state, problem, path):
    if problem.GOAL_TEST(state):
        return []

    if state in path:
        return None  # failure (loop detected)

    for action in problem.ACTIONS(state):
        plan = AND_SEARCH(problem.RESULT(state, action), problem, path + [state])

        if plan is not None:
            return [action, plan]

    return None

#AND search ensures we succeed in all outcomes
def AND_SEARCH(states, problem, path):
    plan = {}

    for s in states:
        subplan = OR_SEARCH(s, problem, path)
        #Recursively call OR_SEARCH to find a plan for that state.

        if subplan is None:
            return None  # failure

        plan[s] = subplan

    return plan


# PRINTING FUNCTION
def PRINT_PLAN(plan, indent=0):
    if plan == []:
        print("  " * indent + "Goal reached")
        return

    action, subplan = plan
    print("  " * indent + f"Action: {action}")

    if isinstance(subplan, dict):  # AND node
        for state, p in subplan.items():
            print("  " * (indent + 1) + f"If state becomes {state}:")
            PRINT_PLAN(p, indent + 2)
    else:
        PRINT_PLAN(subplan, indent + 1)


# MAIN EXECUTION
if __name__ == "__main__":
    initial_state = ('A', 'Dirty', 'Dirty')

    problem = VacuumProblem(initial_state)

    plan = AND_OR_GRAPH_SEARCH(problem)

    print("\n===== ERRATIC VACUUM CLEANER PLAN =====")
    print("Initial State:", initial_state)
    print("\nConditional Plan:\n")

    if plan is None:
        print("No plan found.")
    else:
        PRINT_PLAN(plan)
