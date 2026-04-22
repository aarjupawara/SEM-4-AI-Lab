def solve_crypto():
    letters = ('S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y')  #Tuple of variables
    domains = {l: list(range(10)) for l in letters}

    domains['S'] = list(range(1, 10)) # Leading letters cannot be 0
    domains['M'] = list(range(1, 10))

    def check_math(assignment):
        # Only check when all letters have a value
        if len(assignment) == len(letters):
            s, e, n, d = assignment['S'], assignment['E'], assignment['N'], assignment['D']
            m, o, r, y = assignment['M'], assignment['O'], assignment['R'], assignment['Y']

            #Convert words → numbers
            return (1000*s + 100*e + 10*n + d) + (1000*m + 100*o + 10*r + e) == (10000*m + 1000*o + 100*n + 10*e + y)
        return False

    def backtrack(assignment):
        if len(assignment) == len(letters):
            return assignment if check_math(assignment) else None
        
        # Alldiff constraint
        remaining = [l for l in letters if l not in assignment]
        var = remaining[0]
        
        for val in domains[var]:
            if val not in assignment.values(): # Alldiff check, No two letters share same digit
                assignment[var] = val
                res = backtrack(assignment) #Recursive call
                if res: return res
                del assignment[var] #Backtrack
        return None

    return backtrack({})

print("Cryptarithmetic Solution:", solve_crypto())