# Python built-in libraries
import sys
import time

# User scripts
from domain_independent import general_search
from domain_dependent import *
from solver_library import *

###############################################################################
# MAIN UNINFORMED

if len(sys.argv) != 3:
    print("Number of arguments is wrong.")
    print("Usage: python solver.py -[u | i] <problem.txt>")
    sys.exit(2)

file_name = sys.argv[2] # input file
heuristic_info = sys.argv[1] # if it is informed or uninformed - isto é necessário?

if sys.argv[1] =='-u':
    problem = read_file(file_name) # Problem statement

    strategy = {'search': uniform_cost, 'heuristic': uninformed_heuristic}
    # Chosen uniform cost for uninformed strategy
    # uninformed_heuristic is a dummy function, it will always return 0
    # start_time = time.time()

    #fazer, se houver tempo...
    #strategy = {'search': backtracking, 'heuristic': uninformed_heuristic}
    #strategy = {'search': bidirectional, 'heuristic': uninformed_heuristic}

else:
    if sys.argv[1] =='-i':
        print("Depois aqui ele vai fazer o informed...")
        #blabla(heuristic_info) - não me parece que isto seja necessário...
    else:
        print(sys.argv[1], "is not a recognized flag.")
        print("Usage: python solver.py -[u | i] <problem.txt>")
        sys.exit(3)

print("------------------------------------------------------------------------")
solution = general_search(problem, strategy)

# time = time.time() - start_time

print(solution)
