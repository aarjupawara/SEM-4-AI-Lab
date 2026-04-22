
class Prop:
    def __init__(self, label):
        self.neg = label.startswith('~')
        self.name = label[1:] if self.neg else label

    def get_value(self, assignment):
        val = assignment[self.name]
        return not val if self.neg else val

    def __str__(self):
        return ('~' if self.neg else '') + self.name


def logic(op, x, y):
    if op == '∧':
        return x and y
    if op == '∨':
        return x or y
    if op == '→':
        return (not x) or y
    if op == '↔':
        return x == y



priority = {'∧': 3, '∨': 2, '→': 1, '↔': 1}


def to_postfix(expr):
    out, stk = [], []

    for token in expr:
        if isinstance(token, Prop):
            out.append(token)

        elif token == '(':
            stk.append(token)

        elif token == ')':
            while stk and stk[-1] != '(':
                out.append(stk.pop())
            stk.pop()

        else:
            while stk and stk[-1] != '(' and priority[token] <= priority[stk[-1]]:
                out.append(stk.pop())
            stk.append(token)

    while stk:
        out.append(stk.pop())

    return out

def solve(postfix, values):
    stack = []

    for t in postfix:
        if isinstance(t, Prop):
            stack.append(t.get_value(values))
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(logic(t, a, b))

    return stack[0]

def all_cases(symbols):
    names = sorted({s.name for s in symbols})
    total = 2 ** len(names)

    cases = []
    for i in range(total):
        temp = {}
        for j, n in enumerate(names):
            temp[n] = bool((i >> j) & 1)
        cases.append(temp)

    return names, cases


def show_table(expr, symbols):
    postfix = to_postfix(expr)
    names, cases = all_cases(symbols)

    expr_str = " ".join(str(x) for x in expr)

    print("\nExpression:", expr_str)
    print(" | ".join(names) + " | Result")
    print("-" * (len(names) * 4 + 10))

    for case in cases:
        res = solve(postfix, case)
        row = ["T" if case[n] else "F" for n in names]
        print(" | ".join(row) + " | " + ("T" if res else "F"))


P = Prop('P')
Q = Prop('Q')
R = Prop('R')


e1 = [Prop('~P'), '→', Q]
e2 = [Prop('~P'), '∧', Prop('~Q')]
e3 = [Prop('~P'), '∨', Prop('~Q')]
e4 = [Prop('~P'), '→', Prop('~Q')]
e5 = [Prop('~P'), '↔', Prop('~Q')]
e6 = ['(', P, '∨', Q, ')', '∧', '(', Prop('~P'), '→', Q, ')']
e7 = ['(', P, '∨', Q, ')', '→', Prop('~R')]
e8 = [
    '(', '(', P, '∨', Q, ')', '→', Prop('~R'), ')',
    '↔',
    '(', '(', Prop('~P'), '∧', Prop('~Q'), ')', '→', Prop('~R'), ')'
]
e9 = [
    '(', '(', P, '→', Q, ')', '∧', '(', Q, '→', R, ')', ')',
    '→',
    '(', Q, '→', R, ')'
]
e10 = [
    '(', P, '→', '(', Q, '∨', R, ')', ')',
    '→',
    '(', Prop('~P'), '∧', Prop('~Q'), '∧', Prop('~R'), ')'
]



for expr, syms in [
    (e1, [P, Q]), (e2, [P, Q]), (e3, [P, Q]),
    (e4, [P, Q]), (e5, [P, Q]), (e6, [P, Q]),
    (e7, [P, Q, R]), (e8, [P, Q, R]),
    (e9, [P, Q, R]), (e10, [P, Q, R])
]:
    show_table(expr, syms)
