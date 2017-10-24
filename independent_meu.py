from library_uninformed import *
from dependent_common import *
from utility import *

######################################################################
# general_search
#   function where is implemented the general search algorithm
#input: problem, strategy
#output: solution, cost

def general_search(problem, strategy):

    node = Node()                   # defining first node
    node.state = 0                  # at the start, there is nothing in space

    frontier = [node]               # list of nodes on the frontier
    explored = []                   # list of nodes explored

    n = 0

    #Main cycle
    while True:

        if not frontier: # Empty frontier - error
            solution = 'Solution not found\n'
            cost = 0
            break

        node = choose_node(frontier, strategy) # Choose node to be explored

        goal = goal_check(node.state, problem)

        if goal == 1:               # achieved goal
            solution, cost = generate_answer(node)
            break

        else:                       # goal not achieved: continue exploring

            # Expand all possible nodes reachable from the current node
            frontier, explored = expand_node(frontier, explored, node, problem, strategy)

            explored.append(node)   # node has now been explored
            if node in frontier:
                frontier.remove(node)

    n = len(explored) + 1 # expanded nodes
    # print('N = ' + str(n))

    return solution, cost
