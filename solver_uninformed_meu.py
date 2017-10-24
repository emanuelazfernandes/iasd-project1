# Python built-in libraries
import sys
import time

# User scripts
#from independent_meu import general_search
from dependent_common_meu_try import *
from library_uninformed_meu import *

###############################################################################
# MAIN UNINFORMED

if len(sys.argv) != 3:
    print("Number of arguments is wrong, please enter 2 arguments.")
    sys.exit(2)

file_name = sys.argv[2] # input file
heuristic_info = sys.argv[1] # if it is informed or uninformed

if sys.argv[1] =='-u':
    problem = read_file(file_name) # Problem statement

    strategy = {'search': uniform_cost, 'heuristic': uninformed_heuristic}
    # Chosen uniform cost for uninformed strategy
    # uninformed_heuristic is a dummy function, it will always return 0
    # start_time = time.time()

#solution, cost = general_search(problem, strategy)

# time = time.time() - start_time

#print (solution + str(cost))
