# Vertex Cover Solver

The project's goal is to solve the VERTEX COVER problem in the best computational time.

## What is new ?

This second version includes the following changes:
* Data structure :
    - Changing from local np.array list of edges to global dictionary incidence list 
    - Adding a global list that contains at index i all the vertices of degree i
    - Adding 2 global integers: highest degree and number of non-deleted vertices in the graph 
* Algorithm :
    - Graph preprocessing by adding to the vertex cover the neighbors of all degree 1 vertices
    - Refined search tree 
    - Clique-cover lower bound (clique cover created starting with lowest degree vertex)

## Download of test instances

The following command needs to be run in the "alg-eng-rosty-binetruy-1" directory.

```bash
curl -O http://fpt.akt.tu-berlin.de/alg-eng-data/data.zip
unzip data.zip
```

## Usage

```bash
bash run.sh
```

The benchmark.sh file is being called and its console output is saved into two timestamped files:
 - ./history/yyyymmddHHMM_run_history.txt
 - ./history/yyyymmddHHMM_run_history.csv
