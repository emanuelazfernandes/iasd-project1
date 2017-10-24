################################################################################
# uniform_cost
#   Finds the node in the frontier with the minimum g function
# input: frontier
# output: node index on the frontier

def uniform_cost (frontier):

    min_g = frontier[0].g

    n_node = 0
    i = 0

    for n in frontier:

        if n.g < min_g:
            min_g = n.g
            n_node = i

        i += 1

    return n_node

################################################################################
# uninformed_heuristic
#   Dummy heuristic function - always return 0 (uninformed search)
# input: state, problem class
# output: 0
def uninformed_heuristic(state, problem):

    return 0
