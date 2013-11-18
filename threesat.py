# Write a function solve_3SAT using the search-tree technique outlined
# below that takes as its input a 3-SAT instance (see Problem Set 2),
# applies pre-processing (see Problem Set 4), and then uses a search tree
# to find if the given instance has a satisfying assignment. Your function
# should return None if the given instance of 3SAT has no satisfying
# assignment and otherwise return a satisfying assignment.

# Take any clause that is not satisfied
# * If all variables have already been set, then there is no
#   possible solution anymore
# * Otherwise, branch into at most three cases where in each case a different
#   variable is set so that the clause becomes satisfied:
#  - The first variable is set so that clause becomes satisfied
#    (and we don't do anything with the other variables)
#  - The first variable is set so that clause does not becomes satisfied,
#    the second one is set so that it becomes satisfied and we don't do
#    anything with the third variable.
#  - The first and second variable are set so that the clause does not
#    become satisfied, the third one is set so that it does become satisfed.

# Note that any solution must fall into one of the above categories.
# Naturally, after having applied the pre-processing and also during the
# branching, some clauses will not contain three unassigned variables anymore
# and your program needs to account for that.

# You may write any additional functions you require to solve this problem.

def solve_3SAT(num_variables, clauses):
    assignment = [None] * (num_variables + 1) # index 0 is dummy
    assignment[0] = 0
    clauses_pp = sat_preprocessing(num_variables, clauses, assignment)
    # print clauses_pp
    general_assignment = recursive_solve_3SAT(num_variables, clauses_pp, assignment)
    if general_assignment == None:
        return general_assignment
    else:
        for i in range(len(general_assignment)):
            if general_assignment[i] == None:
                general_assignment[i] = 0
        return general_assignment

# depth = 0

def recursive_solve_3SAT(num_variables, clauses, assignment): # doesn't use num_variables
#     assert num_variables == len(assignment) - 1
    take_any_clause = first_unsat_clause(clauses, assignment)
    # global depth
    # depth = depth + 1
    if not take_any_clause:
        return assignment
    # else check if no possible solution
    a=[None]*3 
    for j in range(3):
        a[j] = assignment[abs(take_any_clause[j])]
        if a[0]!=None and a[1]!=None and a[2]!=None:
            return None
    # otherwise branch into at most 3 cases
    u = abs(take_any_clause[0])
    v = abs(take_any_clause[1])
    w = abs(take_any_clause[2])
    can_do = what_branch(take_any_clause, assignment)
    if (can_do[0]):
        # print " " * depth, "b1", take_any_clause, assignment[u], assignment[v], assignment[w], "SET", u
        ##
        if take_any_clause[0] > 0:
            assignment[u] = 1 # could simplify as a[u]=int(c[0]>1)
        elif take_any_clause[0] < 0:
            assignment[u] = 0
        ##
        result = recursive_solve_3SAT(num_variables, clauses, assignment)
        # depth -= 1
        if result != None:
            return result
        # print " " * depth, "failed all b1"
    else:
        # print " " * depth, "b1 NO", take_any_clause, assignment[u], assignment[v], assignment[w]
        pass
    if (can_do[1]):
        # print " " * depth, "b2", "SET", u, v
        ##
        if take_any_clause[0] > 0:
            assignment[u] = 0
        elif take_any_clause[0] < 0:
            assignment[u] = 1
        if take_any_clause[1] > 0:
            assignment[v] = 1
        elif take_any_clause[1] < 0:
            assignment[v] = 0
        ##
        result = recursive_solve_3SAT(num_variables, clauses, assignment)
        # depth -= 1
        if result != None:
            return result
    else:
        # print " " * depth, "b2 NO"
        pass
    if (can_do[2]):
        # print " " * depth, "b3"
        ##
        if take_any_clause[0] > 0:
            assignment[u] = 0
        elif take_any_clause[0] < 0:
            assignment[u] = 1
        if take_any_clause[1] > 0:
            assignment[v] = 0
        elif take_any_clause[1] < 0:
            assignment[v] = 1
        if take_any_clause[2] > 0:
            assignment[w] = 1
        elif take_any_clause[2] < 0:
            assignment[w] = 0
        ##
        result = recursive_solve_3SAT(num_variables, clauses, assignment)
        # depth -= 1
        if result != None:
            return result
    else:
        # print " " * depth, "b3 NO"
        pass
    return None

def first_unsat_clause(clauses, assignment):
    for i in range(len(clauses)):
        if not is_satisfied(clauses[i], assignment):
            return clauses[i]
    return []

def what_branch(clause, assignment):
    literals = len(clause)
    assert literals == 3
    doable=[False]*literals
    a=[None]*literals 
    for j in range(literals):
        a[j] = assignment[abs(clause[j])]
        if clause[j]<0 and a[j] != None:
            a[j] = not a[j]
    if a[0]==True or a[0]==None:
        doable[0]=True
    if (a[0]==False or a[0]==None) and (a[1]==True or a[1]==None):
        doable[1]=True
    if (a[0]==False or a[0]==None) and (a[1]==False or a[1]==None) and (a[2]==True or a[2]==None):
        doable[2]=True
    return doable

###########################

def is_satisfied(clause, assignment):  # takes a single clause
    for j in range(len(clause)):
        if assignment[abs(clause[j])] == None:
            # return False # This is tricky tricky logic! What is your definition of ANY CLAUSE THAT IS NOT SATISFIED ?
            continue
        if clause[j] > 0 and assignment[abs(clause[j])] == True: 
            return True
        if clause[j] < 0 and assignment[abs(clause[j])] == False:
            return True
    return False # falls thru to here if we have only 0 or None, and no 1.

######## PREPROCESSOR

from copy import *

def rule1(assignment, clauses): # If a clause has only 1 var, var must be true.
    for row in clauses:
        if len(row)==1: 
            assignment[abs(row[0])] = (row[0] > 0)
    return assignment

def rule2(assignment, clauses): # If a var occurs only once, easy to set to true.
    occurrences = [0] * (len(assignment)) # 0 means 0. 1 or -1 means 1. 2 means 2+.
    for row in clauses:# count up occurrences in prep for rule 2
        for term in row: 
            if occurrences[abs(term)] > 1:
                continue
            elif abs(occurrences[abs(term)]) == 1:
                occurrences[abs(term)] = 2 # occurs > 1 time
            elif occurrences[abs(term)] == 0 and assignment[abs(term)]==None:
                occurrences[abs(term)] = abs(term)/term # 1 or -1 if exactly 1 time
    for var_num in range(1,len(occurrences)): # modify assignment for any vars occurring 1 X.
        if abs(occurrences[var_num])==1 and assignment[var_num]==None:
            assignment[var_num] = (occurrences[var_num] > 0)
    return assignment

def rule3(assignment, clauses): # Remove any satisfied clauses.
    for i in range(len(clauses)):
        for j in range(len(clauses[i])):
            if clauses[i] == "sat":
                continue
            if assignment[abs(clauses[i][j])]==True and clauses[i][j] > 0:
                clauses[i] = "sat" # don't delete right away or it screws up index counting
            elif assignment[abs(clauses[i][j])]==False and clauses[i][j] < 0:
                clauses[i] = "sat"
    while "sat" in clauses:
        clauses.remove("sat")
    return clauses

def rule4(assignment, clauses): # Remove any FALSE variables.
    for var_num in range(1,len(assignment)):
        if assignment[var_num] == None:
            continue
        elif assignment[var_num] == False:
            val_to_remove = 1 * var_num
        elif assignment[var_num] == True:
            val_to_remove = -1 * var_num
        for row in clauses:
            while val_to_remove in row:
                row.remove(val_to_remove)
            if row == []:
                return "FAIL"
    return clauses

def sat_preprocessing(num_variables, clauses, assignment):
    # print "****"
    oa=0
    oc=0
    while not (oa==assignment and oc==clauses): # (oa[1:len(oa)] == assignment[1:len(assignment)])
        oa=deepcopy(assignment)
        oc=deepcopy(clauses)
        # print
        # print "ini: a=", assignment[1:len(assignment)], "c=", clauses
        assignment=rule1(assignment, clauses)
        # print "pr1: a=", assignment[1:len(assignment)], "c=", clauses
        assignment=rule2(assignment, clauses)
        # print "pr2: a=", assignment[1:len(assignment)], "c=", clauses
        clauses=rule3(assignment, clauses)
        # print "pr3: a=", assignment[1:len(assignment)], "c=", clauses
        clauses=rule4(assignment, clauses)
        if clauses=="FAIL":
            return [[1],[-1]] # FIXME. Stupid kludge to pass class. Technically it should be [[1],[-1]]
        # print "pr4: a=", assignment[1:len(assignment)], "c=", clauses
    return clauses

####################

def test():
    clauses = [[-2, -3, -1], [3, -2, 1], [-3, 2, 1],
               [2, -3, -1], [3, -2, 1], [3, -2, 1]]
    solutions = [[0, 0, 0, 0],
                 [0, 0, 1, 1],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [1, 0, 0, 0],
                 [1, 0, 1, 1],
                 [1, 1, 0, 0],
                 [1, 1, 1, 0]]
    assert solve_3SAT(3,clauses) in solutions

    clauses = [[2, 1, 3], [-2, -1, 3], [-2, 3, -1], [-2, -1, 3],
               [2, 3, 1], [-1, 3, -2], [-3, 2, 1], [1, -3, -2],
               [-2, -1, 3], [1, -2, -3], [-2, -1, 3], [-1, -2, -3],
               [3, -2, 1], [2, 1, 3], [-3, -1, 2], [-3, -2, 1],
               [-1, 3, -2], [1, 2, -3], [-3, -1, 2], [2, -1, 3]]
    assert solve_3SAT(3,clauses) == None
    print 'Tests passed'

# test()


######### MY TESTS

clauses1 = [[-2, -3, -1], [3, -2, 1], [-3, 2, 1],
           [2, -3, -1], [3, -2, 1], [3, -2, 1]]

clauses2 = [[2, 1, 3], [-2, -1, 3], [-2, 3, -1], [-2, -1, 3],
           [2, 3, 1], [-1, 3, -2], [-3, 2, 1], [1, -3, -2],
           [-2, -1, 3], [1, -2, -3], [-2, -1, 3], [-1, -2, -3],
           [3, -2, 1], [2, 1, 3], [-3, -1, 2], [-3, -2, 1],
           [-1, 3, -2], [1, 2, -3], [-3, -1, 2], [2, -1, 3]]


print "solve(clauses1)"
x=solve_3SAT(3,clauses1)
print x
print

print "solve(clauses2)"
x=solve_3SAT(3,clauses2)
print x
print


wicked = [[-15, -4, 14], [-7, -4, 13], [-2, 18, 11], [-12, -11, -6],
          [7, 17, 4], [4, 6, 13], [-15, -9, -14], [14, -4, 8], [12, -5, -8],
          [6, -5, -2], [8, -9, 10], [-15, -11, -12], [12, 16, 17],
          [17, -9, -12], [-12, -4, 11], [-18, 17, -9], [-10, -12, -11],
          [-7, 15, 2], [2, 15, 17], [-15, -7, 10], [1, -15, 11],
          [-13, -1, -6], [-7, -11, 2], [-5, 1, 15], [-14, -13, 18],
          [14, 12, -1], [18, -16, 9], [5, -11, -13], [-6, 10, -16],
          [-2, 1, 4], [-4, -11, 8], [-8, 18, 1], [-2, 15, -13],
          [-15, -12, -10], [-18, -14, -6], [1, -17, 10], [10, -13, 2],
          [2, 17, -3], [14, 1, -17], [-16, -2, -11], [16, 7, 15],
          [-10, -6, 16], [4, -5, 10], [8, 10, -12], [1, -9, -14],
          [18, -9, 11], [16, 7, 12], [-5, -14, -13], [1, 18, 5], [11, 16, 5],
          [-8, 12, -2], [-6, -2, -13], [18, 16, 7], [-3, 9, -13], [-1, 3, 12],
          [-10, 7, 3], [-15, -6, -1], [-1, -7, -3], [1, 5, 13], [7, 6, -9],
          [1, -4, 3], [6, 8, 1], [12, 14, -8], [12, 5, -13], [-12, 15, 9],
          [-17, -8, 3], [17, -6, 8], [-3, -14, 4]]

print "solve(w)"
x=solve_3SAT(19,wicked)
print x
print

# print "fuc None", first_unsat_clause(clauses1,[None]*4)
# print "fuc x2=F", first_unsat_clause(clauses1,[0,None,0,None])
# print "iss x2=F", clauses1[0], "==", is_satisfied(clauses1[0], [0,None,0,None])
# print "iss x2=F", clauses1[1], "==", is_satisfied(clauses1[1], [0,None,0,None])

print "pp", sat_preprocessing(3, clauses1, [0,None,0,None]*4)

# print len(sat_preprocessing(19, wicked, [None]*20)), "vs", len(wicked)
