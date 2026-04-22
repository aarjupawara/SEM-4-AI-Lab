from collections import deque

# CSP Class
class CSP:
    def __init__(self, variables, domains, neighbors, constraint):
        self.variables = variables #list
        self.domains = domains     #dict
        self.neighbors = neighbors  #graph
        self.constraint = constraint #function defining rules


# Constraint Function
def different_values_constraint(Xi, x, Xj, y):
    return x != y #Two connected variables must have different values


# REVISE
def revise(csp, Xi, Xj): #Make Xi consistent with Xj
    revised = False
    removed = []

    for x in csp.domains[Xi][:]:
        # Check if there is NO value y in Xj satisfying constraint
        if not any(csp.constraint(Xi, x, Xj, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
            removed.append(x)

    return revised, removed 
#revised: whether domain changed, removed: which values removed


# AC-3 Algorithm
def AC3(csp, trace_limit=5):
    queue = deque([(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]]) #Create all arcs (Xi → Xj)

    trace = []
    checks = 0

    while queue:
        Xi, Xj = queue.popleft()
        checks += 1

        before = csp.domains[Xi][:]
        revised, removed = revise(csp, Xi, Xj)
        after = csp.domains[Xi][:]

        # Trace (same as your logic)
        if checks <= trace_limit:
            if revised:
                trace.append(
                    f"Arc ({Xi},{Xj}) checked\n"
                    f"  dom({Xi}) before: {before}\n"
                    f"  removed: {removed}\n"
                    f"  dom({Xi}) after : {after}"
                )
            else:
                trace.append(
                    f"Arc ({Xi},{Xj}) checked\n"
                    f"  dom({Xi}): {before}\n"
                    f"  no change"
                )

        if revised:
            if not csp.domains[Xi]:
                return False, trace

            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    return True, trace


# Problem Definition
variables = ["P1", "P2", "P3", "P4", "P5", "P6"]

neighbors = {
    "P1": ["P2", "P3", "P6"],
    "P2": ["P1", "P3", "P4"],
    "P3": ["P1", "P2", "P5"],
    "P4": ["P2", "P6"],
    "P5": ["P3", "P6"],
    "P6": ["P1", "P4", "P5"],
}


def initial_domains():
    return {v: ["R1", "R2", "R3"] for v in variables}


# CASE 1
print("=== Case 1: Initial domains ===")

domains1 = initial_domains()
csp1 = CSP(variables, domains1, neighbors, different_values_constraint)

result1, trace1 = AC3(csp1)

print("First 5 arc checks:")
for i, step in enumerate(trace1, 1):
    print(f"{i}. {step}")

print("Arc Consistent:", result1)
print("Domains:", csp1.domains)


# CASE 2
print("\n=== Case 2: P1 = R1 ===")

domains2 = initial_domains()
domains2["P1"] = ["R1"]

csp2 = CSP(variables, domains2, neighbors, different_values_constraint)

result2, trace2 = AC3(csp2)

print("First 5 arc checks:")
for i, step in enumerate(trace2, 1):
    print(f"{i}. {step}")

print("Arc Consistent:", result2)
print("Domains:", csp2.domains)

if result2:
    print("Conclusion: No failure (consistent domains exist)")
else:
    print("Conclusion: Failure (empty domain found)")
