from sudoku import Sudoku
import sys


def ac3(sudoku):

    queue = list(sudoku.constraints)

    while queue:

        xi, xj = queue.pop(0)

        if revise(sudoku, xi, xj):  # if we are changing the domain

            if len(sudoku.domains[xi]) == 0:
                return False  # sudoku cannot be formed
            
            for xk in sudoku.neighbors[xi]:
                
                if xk != xi:
                    queue.append([xk, xi])

    return True


def revise(sudoku, xi, xj):

    revised = False

    for x in sudoku.domains[xi]:

        if not any([sudoku.constraint(x, y) for y in sudoku.domains[xj]]):
            sudoku.domains[xi].remove(x)
            revised = True
# Takes out all the elements in domain of xi which are present in xj ie reduces the DOMAIN
    return revised


def backtrack(assignment, sudoku):

    if len(assignment) == len(sudoku.variables):
        #already solved
        return assignment

    var = select_unassigned_variable(assignment, sudoku)

    for value in order_domain_values(sudoku, var):

        if sudoku.consistent(assignment, var, value):

            sudoku.assign(var, value, assignment)

            result = backtrack(assignment, sudoku)
            if result:
                return result

            sudoku.unassign(var, assignment)

    return False


# Most Constrained 
def select_unassigned_variable(assignment, sudoku):
    unassigned = [v for v in sudoku.variables if v not in assignment]
    return min(unassigned, key=lambda var: len(sudoku.domains[var]))


# Least Constraining Value heuristic
# Prefers the value that rules out the fewest choices for the neighboring variables in the constraint graph.
def order_domain_values(sudoku, var):
    if len(sudoku.domains[var]) == 1:
        return sudoku.domains[var]

    return sorted(sudoku.domains[var], key=lambda val: sudoku.conflicts(sudoku, var, val))


def main():
    input=open('input.txt','r')
    puzzle=input.read() 
    if (len(puzzle)<81):
        print("Invalid puzzle")
        sys.exit()
    sudoku = Sudoku(puzzle)



    if ac3(sudoku):

        if sudoku.solved():
            output = open('output.txt', 'w')
            i=0
            for var in sudoku.variables:
                i=1+i
                output.write(str(sudoku.domains[var][0]))
                if(i%3==0):
                    output.write("\t")
                if(i%9==0):
                    output.write("\n")
                    if(i%27==0):
                        output.write("\n")

            output.close()

        else:
            assignment = {}

            for x in sudoku.variables:
                #fills up spaces where only 1 ele is present in domain
                if len(sudoku.domains[x]) == 1:
                    assignment[x] = sudoku.domains[x][0]

            assignment = backtrack(assignment, sudoku)

            for d in sudoku.domains:
                sudoku.domains[d] = assignment[d] if len(d) > 1 else sudoku.domains[d]

            if assignment:

                output = open('output.txt', 'w')
                i=0
                for var in sudoku.variables:
                    i=1+i
                    output.write(str(sudoku.domains[var]))
                    if(i%3==0):
                        output.write("\t")
                    if(i%9==0):
                        output.write("\n")
                        if(i%27==0):
                            output.write("\n")

                    
                output.close()

            else:
                print ("No solution exists")


if __name__ == '__main__':
    main()

