from constraint import Problem

problem = Problem()

problem.addVariables(('x', 'y', 'z'), (0, 1))
problem.addConstraint(lambda x, y, z: x + y + z == 1, {'x', 'y', 'z'})
problem.addConstraint(lambda x, y: x + y == 1, {'x', 'y'})

print("Domains of variables before solving:")
for var, domain in problem._variables.items():
    print(f"{var}: {list(domain)}")

solutions = problem.getSolutions()
print(solutions)
