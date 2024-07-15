Determining when sleuth has been found:

Try all of the possible sleuth settings i.e. set sleuth-red-opal-pair to 1, etc. 
If there is a unique sleuth setting, s.t. all other sleuth settings cause the CSP to be unsolvable,
you can safely say that you know the sleuth answer.

---

Re-using work from previous calculations:

OR-Tools supports hints. So when a constraint is added, use the previous solution as a hint
and then solve with the new constraint.

OR-Tools also supports conditional constraints.
model.Add(x + y + z == 2).OnlyEnforceIf(remove_constraint.Not())

But, python-constraint has hideValue popState and pushState on domain.

---

Flow:

1. Initialize with base constraints.
2. Get a solution called sol_no_sleuth_restrict, using sol_no_sleuth_restrict as a hint if it exists.
3. Try setting sleuth to a certain value and seeing if that is the unique feasible value.
If it is, you found the sleuth. If it isn't, wait for the next constraint, and
then go to step 2. 
