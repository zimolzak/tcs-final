clauses = [[-2, -3, -1], [3, -2, 1], [-3, 2, 1],
           [2, -3, -1], [3, -2, 1], [3, -2, 1]]

assignment = [None, True, None, None]

def what_branch(clause, assignment):
    literals = len(clause)
    assert literals == 3
    doable=[False]*literals
    a=[None]*literals 
    for j in range(literals):
        a[j] = assignment[abs(clause[j])]
        if clause[j]<0 and a[j] != None:
            a[j] = not a[j]
    # print "a", a
    if a[0]==True or a[0]==None:
        doable[0]=True
    if (a[0]==False or a[0]==None) and (a[1]==True or a[1]==None):
        doable[1]=True
    if (a[0]==False or a[0]==None) and (a[1]==False or a[1]==None) and (a[2]==True or a[2]==None):
        doable[2]=True
    return doable

da = what_branch(clauses[0], assignment)

def print_clause(clause):
    literals = len(clause)
    assert literals == 3
    str = [""]*literals
    for j in range(literals):
        if clause[j] < 1:
            str[j] = "not"
    print str[0], "x", abs(clause[0]), "and", str[1], "x", abs(clause[1]), "and", str[2], "x", abs(clause[2])


def print_assignment(assignment):
    strings = []
    for i in range(1,len(assignment)):
        strings.append("x" + str(i) + "=" + str(assignment[i]) )
    print strings


print_clause(clauses[0])

print_assignment(assignment)

print  "doable", da

