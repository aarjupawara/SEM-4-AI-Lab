
from itertools import combinations

def resolve(ci, cj):
    resolvents = set()

    for lit in ci:
        if -lit in cj:
            new_clause = (ci - {lit}) | (cj - {-lit})
            resolvents.add(frozenset(new_clause))

    return resolvents


def resolution(KB, query):
    clauses = set(KB)

    # Add negation of goal
    clauses.add(frozenset([-query]))

    new = set()

    while True:
        pairs = list(combinations(clauses, 2))

        for ci, cj in pairs:
            resolvents = resolve(ci, cj)

            if frozenset() in resolvents:
                return True

            new |= resolvents

        if new.issubset(clauses):
            return False

        clauses |= new


# Q3(a)
KB5 = [
    frozenset([1, 2]),     # P ∨ Q
    frozenset([-1, 3]),    # ¬P ∨ R
    frozenset([-2, 4]),    # ¬Q ∨ S
    frozenset([-3, 4])     # ¬R ∨ S
]

print("Q3(a):", resolution(KB5, 4))  # S


# Q3(b)
KB6 = [
    frozenset([-1, 2]),   # A → B
    frozenset([-2, 3]),   # B → R
    frozenset([-4, -3]),  # S → ¬R
    frozenset([1])        # P
]

print("Q3(b):", resolution(KB6, 4))  # S