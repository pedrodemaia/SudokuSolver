# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:44:49 2020

@author: pedro

Idea: https://www.reddit.com/r/OperationsResearch/comments/hw9kiw/solve_sudoku_using_simulated_annealing_heuristic/
Instances: http://lipas.uwasa.fi/~timan/sudoku/
"""

import numpy as np

def readInstance(name, n=9):
    problem = np.empty([n,n], dtype='int')
    
    f = open('Instances/' + name + '.txt', 'r')
    for i in range(n):
        problem[i] = [int(elem) for elem in f.readline().split(' ')[:-1]]      
    f.close()
    
    return problem
    
if __name__ == '__main__':
    name = 's01a'
    problem = readInstance(name)