from pulp import *
from cvxopt.modeling import variable, op


def optimization_task(cond1, cond2, cond3, cond4, cond5, cond6, cond7, z):
    x_non_negative = (x >= 0)
    problem = op(z, [cond1, cond2, cond3, cond4, cond5, cond6, cond7, x_non_negative])
    problem.solve(solver='glpk')
    print("Minimal transformation price =", problem.objective.value()[0])
    print("Matrix of providing:")
    for i in [1, 5, 9]:
        print('{:<7}{:<7}{:<7}{:<7}'.format(x.value[i-1], x.value[i], x.value[i+1], x.value[i+2]))


def games_theory():
    x1 = pulp.LpVariable('x1', lowBound=0)
    x2 = pulp.LpVariable('x2', lowBound=0)
    x3 = pulp.LpVariable('x3', lowBound=0)
    problem = pulp.LpProblem('0', LpMaximize)
    problem += x1 + x2 + x3, 'Target function'
    problem += 10 * x1 + 6 * x2 + 5 * x3 <= 1, '1'
    problem += 8 * x1 + 7 * x2 + 9 * x3 <= 1, '2'
    problem += 7 * x1 + 5 * x2 + 8 * x3 <= 1, '3'
    problem.solve()
    print('Optimal equipment:')
    for var in problem.variables():
        print(var.name, "=", var.varValue)
    v = value(problem.objective)**(-1)
    print('Sum(x) =', value(problem.objective), '\nv =', v)
    for i in range(len(problem.variables())):
        print('p%d = %f' % (i + 1, problem.variables()[i].varValue * v))
    print()

    y1 = pulp.LpVariable('y1', lowBound=0)
    y2 = pulp.LpVariable('y2', lowBound=0)
    y3 = pulp.LpVariable('y3', lowBound=0)
    problem = pulp.LpProblem('0', LpMinimize)
    problem += y1 + y2 + y3, 'Target function'
    problem += 10 * y1 + 8 * y2 + 7 * y3 >= 1, '1'
    problem += 6 * y1 + 7 * y2 + 5 * y3 >= 1, '2'
    problem += 5 * y1 + 9 * y2 + 8 * y3 >= 1, '3'
    problem.solve()
    print('Optimal modification:')
    for var in problem.variables():
        print(var.name, "=", var.varValue)
    v = value(problem.objective)**(-1)
    print('Sum(y) =', value(problem.objective), '\nv =', v)
    for i in range(len(problem.variables())):
        print('q%d = %f' % (i + 1, problem.variables()[i].varValue * v))
    print()


n = [2, 3, 4, 2, 5, 7, 1, 4, 9, 4, 3, 2]
x = variable(12, 'x')
optimization_task((sum(x[:4]) <= 50), (sum(x[4:8]) <= 30), (sum(x[8:12]) <= 20), (sum(x[::4]) == 30),
                  (sum(x[1::4]) == 30), (sum(x[2::4]) == 10), (sum(x[3::4]) == 20),
                  sum([n1 * x1 for (n1, x1) in zip(n, x)]))
games_theory()
