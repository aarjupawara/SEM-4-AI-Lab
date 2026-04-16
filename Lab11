def backtracking_search(csp):
    return backtrack({}, csp) #empty assignment (nothing assigned yet)

def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables): #If all districts are assigned → solution found
        return assignment
    
    # Select unassigned variable
    var = next(v for v in csp.variables if v not in assignment)
    
    for value in csp.domains[var]:
        if csp.nconflicts(var, value, assignment) == 0: #Only proceed if no conflicts
            csp.assign(var, value, assignment)
            result = backtrack(assignment, csp)
            if result is not None:
                return result
            csp.unassign(var, assignment) #Remove assignment and try next color
    return None #No valid color found → go back further

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])
        return sum(1 for v in self.neighbors[var] if conflict(v)) #Counts how many neighbors conflict

# Problem Instance for Gujarat
districts = ["Kucchh", "Banaskantha", "Patan", "Mehsana", "Sabarkantha", "Gandhi Nagar", 
             "Ahmedabad", "Surendranagar", "Rajkot", "Jamnagar", "Porbandar", "Junagadh", 
             "Amreli", "Bhavnagar", "Anand", "Kheda", "Panchmahal", "Dahod", "Vadodara", 
             "Bharuch", "Narmada", "Surat"]

neighbors = {
    "Kucchh": ["Banaskantha", "Surendranagar", "Jamnagar"],
    "Banaskantha": ["Kucchh", "Patan", "Sabarkantha"],
    "Patan": ["Banaskantha", "Mehsana", "Surendranagar"],
    "Mehsana": ["Patan", "Sabarkantha", "Gandhi Nagar"],
    "Sabarkantha": ["Banaskantha", "Mehsana", "Gandhi Nagar"],
    "Gandhi Nagar": ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Ahmedabad": ["Gandhi Nagar", "Kheda", "Anand", "Surendranagar"],
    "Surendranagar": ["Kucchh", "Patan", "Ahmedabad", "Rajkot", "Bhavnagar"],
    "Rajkot": ["Surendranagar", "Jamnagar", "Junagadh", "Amreli"],
    "Jamnagar": ["Kucchh", "Rajkot", "Porbandar"],
    "Porbandar": ["Jamnagar", "Junagadh"],
    "Junagadh": ["Porbandar", "Rajkot", "Amreli"],
    "Amreli": ["Rajkot", "Junagadh", "Bhavnagar"],
    "Bhavnagar": ["Surendranagar", "Amreli", "Anand"],
    "Anand": ["Ahmedabad", "Bhavnagar", "Kheda", "Vadodara"],
    "Kheda": ["Gandhi Nagar", "Ahmedabad", "Anand", "Panchmahal"],
    "Panchmahal": ["Kheda", "Dahod", "Vadodara"],
    "Dahod": ["Panchmahal"],
    "Vadodara": ["Anand", "Panchmahal", "Bharuch"],
    "Bharuch": ["Vadodara", "Narmada", "Surat"],
    "Narmada": ["Bharuch", "Surat"],
    "Surat": ["Bharuch", "Narmada"]
}

domains = {d: ["Red", "Green", "Blue", "Yellow"] for d in districts}

def map_constraint(A, a, B, b): #Adjacent districts must have different colors
    return a != b

gujarat_csp = CSP(districts, domains, neighbors, map_constraint)
solution = backtracking_search(gujarat_csp)

print("\nGujarat Map Coloring Solution:\n")
print("{:<15} | {:<10}".format("District", "Color"))
print("-" * 28)

for district, color in sorted(solution.items()):
    print("{:<15} | {:<10}".format(district, color))
