# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:44:49 2020

@author: pedro

Idea: https://www.reddit.com/r/OperationsResearch/comments/hw9kiw/solve_sudoku_using_simulated_annealing_heuristic/
Instances: http://lipas.uwasa.fi/~timan/sudoku/

USE SOS
use default optimizer from python
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB

def readInstance(name, n=9):
    problem = np.empty([n,n], dtype='int')
    
    f = open('Instances/' + name + '.txt', 'r')
    for i in range(n):
        problem[i] = [int(elem) for elem in f.readline().split(' ')[:-1]]      
    f.close()
    
    return problem

def getSolution(problem):
    n = len(problem)
    s = int(np.sqrt(n))
    
    model = gp.Model('Sudoku')
    
    # create 9 binary variables for each cell
    var = gp.tupledict()
    for i in range(n):
        for j in range(n):
            if problem[i,j] > 0:
                # set LB to 1 for vrialbes with a given value
                k = problem[i,j] - 1
                var[(i,j,k)] = model.addVar(1, 1, 0, GRB.BINARY, 
                                            name='v[{},{},{}]'.format(i,j,k))
            else:
                for k in range(n):
                    var[(i,j,k)] = model.addVar(0, 1, 0, GRB.BINARY, 
                                            name='v[{},{},{}]'.format(i,j,k))
    
    # Assert each cell assumes one value
    model.addConstrs((var.sum(i, j, '*') == 1
    for i in range(n) for j in range(n)), name = 'cell')
    
    # Assert there are no duplicate values in a row
    model.addConstrs((var.sum(i, '*', k) == 1
    for i in range(n) for k in range(n) if k+1 not in problem[i,:]), 
                 name = 'row')
    
    # Assert there are no duplicate values in a column
    model.addConstrs((var.sum('*', j, k) == 1
    for j in range(n) for k in range(n) if k+1 not in problem[:,j]),
                 name ='column')
    
    # Assert there are no duplicate values in a subgrid
    for si in range(s):
        for sj in range(s):
            for k in range(n):
                if k+1 not in problem[si*s:(si+1)*s,sj*s:(sj+1)*s]:
                    model.addConstr(gp.quicksum(var[i, j, k]
                                for i in range(si*s, (si+1)*s)
                                for j in range(sj*s, (sj+1)*s) 
                                if problem[i,j] == 0) == 1, 
                                name = 'Sub[{},{},{}]'.format(si,sj,k))
                    

    # optimize model
    model.optimize()
    
    # get solution
    sol = model.getAttr('X', var)
    solution = np.empty([n,n], dtype='int')
    for key, val in sol.items():
        if val > 0.5:
            solution[key[0],key[1]] = int(key[2]+1)
    
    return model, solution

def printSolution(solution):
    print ('')
    print ('Solution:')
    print ('')
    print(solution)

def writeLP(model):
    model.write('sudoku.lp')
    
    
if __name__ == '__main__':
    name = 's01a'
    n = 9
    problem = readInstance(name, n)
    
    model, solution = getSolution(problem)
    
    writeLP(model)
    
    printSolution(solution)
    
# =============================================================================
#     model = gp.Model('Sudoku')
#     vars = model.addVars(n, n, n, vtype=GRB.BINARY, name='value')
#     # Fix variables associated with cells whose values are pre - specified
#     for i in range(n):
#         for j in range(n):
#             if problem[i][j] > 0:
#                 val = problem[i][j] - 1
#                 vars[i, j, val].LB = 1
#     
#     # Each cell must take one value
#     model.addConstrs((vars.sum(i, j, '*') == 1
#     for i in range(n) for j in range(n)), name = 'cell')
#     
#     # Each value appears once per row
#     model.addConstrs((vars.sum(i, '*', v) == 1
#     for i in range(n) for v in range(n)), name = 'row')
#     
#     # Each value appears once per column
#     model.addConstrs((vars.sum('*', j, v) == 1
#     for j in range(n) for v in range(n)), name ='column')
#     
#     # Each value appears once per subgrid
#     model.addConstrs((
#     gp.quicksum(vars[i, j, v] for i in range(i0*s, (i0+1)*s)
#     for j in range(j0*s, (j0+1)*s)) == 1
#     for v in range(n)
#     for i0 in range(s)
#     for j0 in range(s)), name = 'Sub')
#     
#     model.optimize()
#     model.write('sudoku.lp')
#     print ('')
#     print ('Solution:')
#     print ('')
#     
#     # get result
#     solution = model.getAttr('X', vars)
#     sol = np.empty([n,n], dtype='int')
#     for i in range(n):
#         for j in range(n):
#             for v in range(n):
#                 if solution[i, j, v] > 0.5:
#                     sol[i,j] = int(v+1)
#     
#     print(sol)
# =============================================================================
    
    
