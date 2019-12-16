from __future__ import print_function

import sys
import time

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

print(g)

def is_edgeless():
    """
    INPUT: None
    is_edgeless returns True if the graph doesn't have any undeleted edges and False otherwise
    OUTPUT: True or False
    """
    return max_degree == 0


def del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'delete'
    del_vert 'deletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in vertices:
        # 'Delete' vertex:
        ###Deleting in g
        g[vertex][0] = True
        nb_vertices -= 1
        ###Deleting in degree_list and updating nb_edges
        degree_vertex = g[vertex][1]
        nb_edges -= degree_vertex
        degree_list[degree_vertex].remove(vertex)
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            ###Updating g
            g[adj_vert][1] -= 1
            if not g[adj_vert][0]:
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert+1].remove(adj_vert)
                degree_list[degree_adj_vert].append(adj_vert)
    #If max_degree is obsolete, go through all degrees decreasing from max_degree to find the new value
    while (max_degree > 0) & (degree_list[max_degree] == []):
        max_degree -= 1


def un_del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'undelete'
    un_del_vert 'undeletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    global max_degree
    global degree_list
    global nb_vertices
    global nb_edges
    for vertex in vertices:
        # 'Undelete' vertex:
        ###Undeleting in g
        g[vertex][0] = False
        nb_vertices += 1
        ###Undeleting in degree_list and updating nb_edges
        degree_vertex = g[vertex][1]
        nb_edges += degree_vertex
        degree_list[degree_vertex].append(vertex)
        # If the vertex has a higher degree than max_degree, we update max_degree
        if g[vertex][1] > max_degree:
            max_degree = g[vertex][1]
        # Update number of edges on adjacent vertices:
        for adj_vert in g[vertex][2]:
            ###Updating g
            g[adj_vert][1] += 1
            if not g[adj_vert][0]:
                ###Updating degree_list
                degree_adj_vert = g[adj_vert][1]
                degree_list[degree_adj_vert-1].remove(adj_vert)
                degree_list[degree_adj_vert].append(adj_vert)
                #If the neighbor has after undeletion a higher degree than max degree we update it
                if g[adj_vert][1] > max_degree:
                    max_degree = g[adj_vert][1]


def really_del_vert(vertices):
    """
    INPUT: vertices is list : vertices to 'delete'
    del_vert 'deletes' the given vertices and updates the number of edges of all adjacent vertices
    """
    for vertex in vertices:
        if not g[vertex][0]: del_vert([vertex])
        for adj_vert in g[vertex][2]:
            g[adj_vert][2].remove(vertex)
        del g[vertex]


def degree_zero_rule(really=True):
    """
    INPUT: None
    degree_zero_rule deletes all degree zero vertices and returns them
    OUTPUT: list
    """
    if degree_list[0] != []:
        degree_zero_rule.counter += 1
        undelete = degree_list[0][:]
        if really: really_del_vert(undelete)
    else: undelete = []
    return undelete



def get_neighbor(vertex):
    """
    INPUT: vertex is str
    get_neighbor returns the first neighbor
    OUTPUT: str
    """
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]:
            return neighbor


def get_degree_one_neighbors():
    """
    INPUT: None
    get_degree_one_neighbors return the neighbors of all vertices of degree one
    (if two vertices of degree one are adjacent to each other, it choses one of them)
    OUTPUT: list
    """
    # Initialize list of neighbors of vertices with one degree:
    neighbors = []
    # Iterate through all vertices of degree one and append its neighbor to the list (if not added already):
    for vertex in degree_list[1]:
        if vertex not in neighbors:
            neighbor = get_neighbor(vertex)
            if neighbor not in neighbors:
                neighbors.append(neighbor)
    return neighbors



def degree_one_rule(really=True):
    """
    INPUT: k is int 
    degree_one_rule deletes all degree one vertices and returns them, deletes all 
    of their neighbors and return them to add them to S. also returns the depth budget k changed by deletion
    OUTPUT: S_kern is list of vertices, undeleteis list of vertices, k is int
    """
    S_kern, undelete = [],[]
    while degree_list[1] != []:
        degree_one_rule.counter += 1
        # Get neighbors of vertices with degree one (if two are adjacent to each other, only one of them):
        degree_one_neighbors = get_degree_one_neighbors()
        S_kern += degree_one_neighbors
        # 'Delete' neighbors of degree one vertices:
        if really: really_del_vert(degree_one_neighbors)
    return S_kern, undelete


def get_all_neighbors(vertex):
    """
    INPUT: vertex
    get_neighbor returns the first neighbor
    OUTPUT: list of vertices
    """
    neighbors = []
    for neighbor in g[vertex][2]:
        if not g[neighbor][0]: neighbors.append(neighbor)
    return neighbors



def merge_vert(vertex, u, w):
    """
    INPUT: vertex of degree 2, and its two neighbors u and w
    to use only if vertex has degree 2 and there is no edge between u and w
    merges vertex and its 2 neighbors, but doesn't change k 
    OUTPUT: the name of the resulting merged_point
    """
    global nb_vertices
    global degree_list
    global max_degree
    merged_point = (vertex, u, w)
    del_vert([vertex, u, w])
    if merged_point in g:
        un_del_vert([merged_point])
        return merged_point
    #add merged vertex and delete vertex and its neighbors
    add_vertex(merged_point)
    nb_vertices += 1
    #add edges towards every neighbor only once 
    for z in [u, w]:
        for n in g[z][2]:
            if n not in g[merged_point][2]:
                if not g[n][0]:
                    add_edge([merged_point, n])
                    n_degree = g[n][1]
                    degree_list[n_degree-1].remove(n)
                    degree_list[n_degree].append(n)
                else:
                    #add edge in dictionary
                    g[merged_point][2].append(n)
                    g[n][2].append(merged_point)
                    g[n][1] += 1
    degree_list[g[merged_point][1]].append(merged_point)
    return merged_point

def degree_two_rule():
    S_kern = []
    if max_degree < 2: return S_kern
    while degree_list[2] != []:
        degree_two_rule.counter += 1
        vertex = degree_list[2][0]
        [u, w] = get_all_neighbors(vertex)
        if w in g[u][2]:
            del_vert([vertex, u, w])
            S_kern += [u, w]
        else:
            merged_point = merge_vert(vertex, u, w)
            S_kern.append(vertex)
    return S_kern


def append_to_S(S, vertices):
    for vertex in vertices:
        if type(vertex) is str:
            S.append(vertex)
        else:
            v, u, w = vertex
            S = del_from_S(S,[v])
            for x in [u, w]:
                S = append_to_S(S, [x])
    return S


def del_from_S(S, vertices):
    for vertex in vertices:
        if type(vertex) is str:
            S.remove(vertex)
        else:
            v, u, w = vertex
            S = append_to_S(S, [v])
            for x in [u, w]:
                S = del_from_S(S, [x])
    return S


def correct_output(S):
    S_new = []
    for vertex in S:
        S_new = append_to_S(S_new, [vertex])
    return S_new


def kernalization():
    """
    INPUT: 
    kernalization applies all the kernelization rules
    OUTPUT: S_kern is list of vertices
    """
    kernalization.counter += 1
    # Execute reduction rules:
    degree_zero_rule()
    S_kern, _ = degree_one_rule()
    S_kern_two= degree_two_rule()
    S_kern += S_kern_two
    # S_kern_dom, _ = domination_rule()
    # S_kern += S_kern_dom
    return S_kern

def bigger_than(neigh, vertex):
    try:
        result = neigh > vertex
        return result
    except:
        if type(vertex) == str and type(neigh) == tuple:
            return True
        if type(vertex) == tuple and type(neigh) == str:
            return False
        if vertex[0] == neigh[0] and vertex[1] == neigh[1]:
            return bigger_than(vertex[2], neigh[2])    
        elif vertex[0] == neigh[0]:
            return bigger_than(vertex[1], neigh[1])
        return bigger_than(vertex[0], neigh[0]) 



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
        my_colnames.append("%s" % (vertex))
        for neigh in g[vertex][2]:
            if bigger_than(neigh, vertex):
                my_rownames.append("e %s %s" % (vertex,neigh))
                rows.append([[vertex,neigh],[1,1]])
    return my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows

def vc_cplex():
    """
    INPUT: None
    prints the vertex cover corresponding to global g using cplex solver
    OUTPUT: None
    """
    degree_zero_rule.counter = 0
    degree_one_rule.counter = 0
    degree_two_rule.counter = 0
    # domination_rule.counter = 0
    kernalization.counter = 0
    S = []
    ###### Kernelization
    start_kern = time.time()
    if not is_edgeless():
        while True:
            S_kern = kernalization()
            if S_kern == []: break
            S += S_kern
    correct_output(S)
    print_result(S)
    ###### CPLEX
    start_cplex = time.time()
    if not is_edgeless():
        #get parameters of the CPLEX problem
        my_obj, my_ub, my_ctype, my_colnames, my_rhs, my_rownames, my_sense, rows = mipParam()
        #initialize the CPLEX problem
        prob = cplex.Cplex()
        #To avoid printing the summary of the cplex resolution, to limit memory usage to 1.5GB and get more precise results on big graphs
        prob.set_results_stream(None)
        prob.parameters.workmem = 1536
        # prob.parameters.mip.tolerances.mipgap = 1e-15
        # prob.parameters.mip.tolerances.absmipgap = 1e-15
        #fill the CPLEX problem with all correct parameters
        prob.objective.set_sense(prob.objective.sense.minimize)
        prob.variables.add(obj=my_obj, ub=my_ub, types=my_ctype, names=my_colnames)
        prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs, names=my_rownames)
        #Solve the CPLEX problem
        prob.solve()
        #print the solution 
        numcols = prob.variables.get_num()
        x = prob.solution.get_values()
        for j in range(numcols):
            if x[j] == 1:
                print(my_colnames[j])
    end = time.time()
    print("#Kern timing: %s" % (start_cplex-start_kern))
    print("#Cplex timing: %s" % (end-start_cplex))   
    print("#degree zero rules: %s" % degree_zero_rule.counter)
    print("#degree one rules: %s" % degree_one_rule.counter) 

vc_cplex()