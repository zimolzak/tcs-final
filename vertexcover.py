from itertools import *

def validity_check(cover, graph):
    uncovered = 0
    for i in range(0, len(graph)):
        for j in range(0, len(graph[i])):
            uncovered = uncovered + graph[i][j] * (not cover[i]) * (not cover[j])
    return not uncovered

def solve_vc(input_graph): # naive algorithm
    n = len(input_graph)
    minimum_vertex_cover = n
    minimum_assignment = [1] * n
    for assignment in product([0,1], repeat=n):
        if validity_check(assignment, input_graph):
            size_of_assig = sum(assignment)
            if size_of_assig < minimum_vertex_cover:
                minimum_vertex_cover = size_of_assig
                minimum_assignment = assignment
    return list(minimum_assignment)
