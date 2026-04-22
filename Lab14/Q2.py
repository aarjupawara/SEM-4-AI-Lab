
def backward_chain(KB, facts, goal, visited=None):
    if visited is None:
        visited = set()

    if goal in facts:
        return True

    if goal in visited:
        return False

    visited.add(goal)

    for premises, conclusion in KB:
        if conclusion == goal:
            if all(backward_chain(KB, facts, p, visited) for p in premises):
                return True

    return False


# Q2(a)
KB3 = [
    (["P"], "Q"),
    (["R"], "Q"),
    (["A"], "P"),
    (["B"], "R")
]

facts3 = ["A", "B"]

print("Q2(a):", backward_chain(KB3, facts3, "Q"))


# Q2(b)
KB4 = [
    (["A"], "B"),
    (["B", "C"], "D"),
    (["E"], "C")
]

facts4 = ["A", "E"]

print("Q2(b):", backward_chain(KB4, facts4, "D"))