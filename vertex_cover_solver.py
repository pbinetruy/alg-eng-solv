from __future__ import print_function

import sys

import cplex
from cplex.exceptions import CplexError


g = {}
max_degree = 0
degree_list = []
nb_vertices = 0
nb_edges = 0

def add_vertex(vertex):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), vertex is str
    add_vertex adds a new vertex with default values
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    g[vertex] = [False, 0, []]


def add_edge(edge):
    """
    INPUT: g is dict with each value list of length 3 (boolean, int, list), edge is list of length 2
    add_vertex adds a new edge to the graph and returns this graph
    OUTPUT: dict with each value list of 3 (boolean, int, list)
    """
    global max_degree
    global nb_edges
    if edge[0] in g and edge[1] in g[edge[0]][2]: return
    #Increment edge counter
    nb_edges += 1
    #add edge in dictionary
    for vertex in edge:
        if not vertex in g.keys():
            add_vertex(vertex)
        g[vertex][1] += 1
        # If current degree is greater than maximum degree, update:
        if g[vertex][1] > max_degree:
            max_degree += 1
    g[edge[0]][2].append(edge[1])
    g[edge[1]][2].append(edge[0])


def get_data():
    """
    INPUT: None
    get_data reads standard input and creates the given graph
    OUTPUT: None
    """
    global degree_list
    global nb_vertices
    # Get standard input:
    input_data = sys.stdin
    for line in input_data:
        if not line[0] == '#':
            # Get current edge and add it to the graph:
            current_edge = line.split()
            add_edge(current_edge)
    nb_vertices = len(g)
    # Initializing degree_list:
    nb_vertices = len(g)
    degree_list = [[] for i in range(nb_vertices)]
    for vertex in g:
        degree = g[vertex][1]
        # Append vertex to the list located at its degree in degree_list:
        degree_list[degree].append(vertex)


def print_result(vertices):
    """
    INPUT: vertices is list : vertices
    print_result prints every given vertex in a new line
    OUTPUT: None
    """
    for vertex in vertices:
        print(vertex)



get_data()
print ("#", g)



def mipParam():
    """
    INPUT: NONE
    Under the assumption that all lists of neighbors are correctly updated, returns all the necessary objects to run CPLEX
    OUTPUT: my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows
    """
    global nb_vertices
    global nb_edges
    #Objective function is sum with all factors set to 1
    my_obj = [1]*nb_vertices
    #all variables bounded by 0 (default) and 1
    my_ub = [1]*nb_vertices
    #All variables are integers
    my_ctype = 'I'*nb_vertices
    #each edge is a greater-than 1 constraint 
    my_rhs = [1]*nb_edges
    my_sense = 'G'*nb_edges
    #name of the vertices and of the columns are left to fill
    my_colnames = []
    my_rownames = []
    #Actual rows are going to be filled during the for loop
    rows = []
    for vertex in g:
        my_colnames.append(vertex)
        for neigh in g[vertex][2]:
            if neigh > vertex:
                my_rownames.append("e %s %s" % (vertex,neigh))
                rows.append([[vertex,neigh],[1,1]])
    return my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows


my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows = mipParam()

prob = cplex.Cplex()

#To avoid printing the summary of the cplex resolution
prob.set_results_stream(None).

prob.objective.set_sense(prob.objective.sense.minimize)

prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype, names=my_colnames)

prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs, names=my_rownames)

prob.solve()

# # solution.get_status() returns an integer code
# print("#Solution status = ", prob.solution.get_status(), ":", end=' ')
# # the following line prints the corresponding string
# print("#", prob.solution.status[prob.solution.get_status()])
# print("#Solution value  = ", prob.solution.get_objective_value())

numcols = prob.variables.get_num()
numrows = prob.linear_constraints.get_num()

slack = prob.solution.get_linear_slacks()
x = prob.solution.get_values()

for j in range(numcols):
    if x[j] == 1:
        print(my_colnames[j])