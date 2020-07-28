# Sudoku Solver

This an optimization solver for the Sudoku game (https://en.wikipedia.org/wiki/Sudoku).

## Formulation

This problem is modelled as a Linear Programming (LP) problem with binary variables:

<img src="https://render.githubusercontent.com/render/math?math=x_{i,j,k} \in \[ 0,1 \] \quad \forall i \in \{1,..,9\} \quad \forall j \in \{1,..,9\} \quad \forall k \in \{1,..,9\}">

There is one variable for for each possible value for each cell in the game. There are no variables for the cells with pre-specified values.

### Constraints

There are four types of constraints in this formulation:

#### 1. Unique value on each cell

This constraint ensures there is only one active variable for each cell.

<img src="https://render.githubusercontent.com/render/math?math=\sum\limits_{k \in \{1,..,9\}} x_{i,j,k} = 1 \quad \forall i \in \{1,..,9\} \quad \forall j \in \{1,..,9\}">

#### 2. Different values on each row

This constraint ensures there are no repeated values on a row.

<img src="https://render.githubusercontent.com/render/math?math=\sum\limits_{j \in \{1,..,9\}} x_{i,j,k} = 1 \quad \forall i \in \{1,..,9\} \quad \forall k \in \{1,..,9\}">

#### 3. Different values on each column

This constraint ensures there are no repeated values on a column.

<img src="https://render.githubusercontent.com/render/math?math=\sum\limits_{i \in \{1,..,9\}} x_{i,j,k} = 1 \quad \forall j \in \{1,..,9\} \quad \forall k \in \{1,..,9\}">

#### 4. Different values on each subgrid

This constraint ensures there are no repeated values on a subgrid.

<img src="https://render.githubusercontent.com/render/math?math=\sum\limits_{i \in \{3 \times si + 1,..,3 \times (si + 1)\}} \sum\limits_{j \in \{3 \times sj + 1,..,3 \times (sj + 1)\}} x_{i,j,k} = 1 \quad \forall si \in \{1,..,3\} \quad \forall sj \in \{1,..,3\} \quad \forall k \in \{1,..,9\}">

### Objective Function

The objective of this problem is to find a feasible solution, therefore there is no objective function.

## Solver

The problem is modelled and solved with Gurobi (https://www.gurobi.com/).

## Intances

The instances were taken from http://lipas.uwasa.fi/~timan/sudoku/
 
