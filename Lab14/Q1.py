
def forward_chain(KB, facts, goal):
    inferred = set(facts)

    while True:
        new_inferred = set()

        for premises, conclusion in KB:
            if conclusion not in inferred:
                if all(p in inferred for p in premises):
                    new_inferred.add(conclusion)

        if not new_inferred:
            break

        inferred |= new_inferred

        if goal in inferred:
            return True

    return goal in inferred


# Q1(a)
KB1 = [
    (["P"], "Q"),
    (["L", "M"], "P"),
    (["A", "B"], "L")
]

facts1 = ["A", "B", "M"]

print("Q1(a):", forward_chain(KB1, facts1, "Q"))


# Q1(b)
KB2 = [
    (["A"], "B"),
    (["B"], "C"),
    (["C"], "D"),
    (["D", "E"], "F")
]

facts2 = ["A", "E"]

print("Q1(b):", forward_chain(KB2, facts2, "F"))
