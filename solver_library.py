################################################################################
# uniform_cost
#   Finds the node in the frontier with the minimum g function
# input: frontier
# output: node index on the frontier

def uniform_cost(frontier):

    min_g = frontier[0].g # cost of first node on the frontier

    n_node = 0
    i = 0

    # search the frontier for the node with the minimum cost
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

# depois, se tiveres tempo, faz estes 2 para comparar e meter no relatório...
def backtracking(frontier):
    #aqui a fronteira é mais pequena, só quando expande o node é que se vai
    # adicionando, seguindo sempre pelo ramo mais profundo (depth first search)
    return 0

def bidirectional(frontier):
    #ui, a serious remake is in order...2 cenas chamadas ao mesmo tempo né?
    return 0
