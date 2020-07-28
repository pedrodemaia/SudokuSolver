# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:44:49 2020

@author: pedro
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
    model.setParam('OutputFlag', False)
    
    # create 9 binary variables for each cell without given value
    var = gp.tupledict()
    for i in range(n):
        for j in range(n):
            if problem[i,j] == 0:
                for k in range(n):
                    var[(i,j,k)] = model.addVar(0, 1, 0, GRB.BINARY, 
                                            name='v[{},{},{}]'.format(i,j,k))
    
    # Assert each cell assumes one value
    model.addConstrs((var.sum(i, j, '*') == 1
    for i in range(n) for j in range(n) if problem[i,j] == 0), name = 'cell')
    
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
    
    if model.Status == GRB.OPTIMAL:
        # get solution
        sol = model.getAttr('X', var)
        solution = problem.copy()
        for key, val in sol.items():
            if val > 0.5:
                solution[key[0],key[1]] = int(key[2]+1)
    else:
        solution = np.zeros([n,n], dtype = 'int')
      
    return model, solution

def printSolution(solution):
    print ('')
    print ('Solution:')
    print ('')
    print(solution)

def writeLP(model):
    model.write('sudoku.lp')
    
    
if __name__ == '__main__':
    name = 's16'
    n = 9
    problem = readInstance(name, n)
    
    model, solution = getSolution(problem)
    
    #writeLP(model)
    
    printSolution(solution)
    
    
