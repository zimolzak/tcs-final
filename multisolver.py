# You are provided with a 'magic' function solve_vc which
# solves VERTEX COVER for a given graph represented as an
# adjacency matrix. It returns a minimum cover of the graph as
# a list of 0s and 1s where 1 means the corresponding
# vertex is in the cover and 0 means it is not.

# You should use solve_vc to write a function multisolve
# which takes as its inputs an adjacency matrix, graph and a
# string problem where problem is 'VERTEX COVER', 'INDEPENDENT SET'
# or 'CLIQUE' and returns a list of 0s and 1s which are assignments
# of the vertices where 1 means the corresponding vertex is in the
# solution to the corresponding problem and 0 means it is not.

# You may code any additional functions you feel necessary
# but solve_vc must be used to solve each problem.

from vertexcover import solve_vc

def multisolve(graph, problem):
    if problem=="VERTEX COVER":
        return solve_vc(graph)
    elif problem=="INDEPENDENT SET":
        min_vc = solve_vc(graph)
        ind_set = []
        for vc_node in min_vc:
            ind_set.append(1 - vc_node)
        return ind_set
    elif problem=="CLIQUE":
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if i==j:
                    continue
                graph[i][j] = 1 - graph[i][j]
        return multisolve(graph, "INDEPENDENT SET")
        return [0]
    else:
        return [0]

def test():
   graph = [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]
   assert multisolve(graph, "VERTEX COVER") == [0,0,1,1]
   assert multisolve(graph, "INDEPENDENT SET") in [[1,0,0,1],[1,1,0,0],[0,1,1,0]]
   assert multisolve(graph, "CLIQUE") in [[1,0,1,0],[0,0,1,1],[0,1,0,1]]

test()

