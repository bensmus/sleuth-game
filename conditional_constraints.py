# from ortools.sat.python import cp_model

# model = cp_model.CpModel()
# solver = cp_model.CpSolver()

# # Variables
# x = model.new_int_var(0, 100, "x")
# y = model.new_int_var(0, 100, "y")
# bool1 = model.new_bool_var('bool1')

# # Constraints
# model.add(x + y <= 30)
# model.add(x == 2*y).only_enforce_if(bool1)

# model.maximize(x + y)

# # Solve
# status = solver.solve(model)
# print(f"x={solver.value(x)},  y={solver.value(y)}")

# model.add(bool1 == 1)

# status = solver.solve(model)
# print(f"x={solver.value(x)},  y={solver.value(y)}")

# model.add(bool1 == 0)

# status = solver.solve(model)
# print(f"x={solver.value(x)},  y={solver.value(y)}")

# from constraint import Domain, Problem, ExactSumConstraint

# N = 36
# domains = [Domain([0, 1]) for _ in range(N)]
# problem = Problem()
# for i in range(N):
#     problem.addVariable(f'var{i}', domains[i])

# domains[5].hideValue(0) # 'var5' has to be 1.
# print(domains[5])
# # problem.addVariable('var5', domains[5]) # Duplicate variable error

# problem.addConstraint(ExactSumConstraint(1), [f'var{i}' for i in range(N)])

# print(problem.getSolution()) # Doesn't restrict var5.
