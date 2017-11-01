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

'''
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
'''

def Astar(frontier):
    #aqui vai chamar a função heuristica para  escolher o node
    min_f = frontier[0].g + frontier[0].h # cost of first node on the frontier

    n_node = 0
    i = 0

    # search the frontier for the node with the minimum cost
    for n in frontier:
        if (n.g + n.h) < min_f:
            min_f = n.g + n.h
            n_node = i

        i += 1

    return n_node

# simple heuristic function that calculates the h cost, based on maximum
# utility for the launch: (node variable cost) * (weight of left vertices)
def heur1(node, problem):

    in_space = node.state.present + node.state.manifest
    #in_space = node.state.present
    w_not_launched = problem.total_weight
    for vertex in in_space:
        w_not_launched -= vertex.w

    h = node.state.launch.vc * w_not_launched
    
    return h

# another simple heuristic function that calculates the h cost, based on
# maximum utility for the launch with the minimum variable cost:
# (launch_with_minimal_vc from rest of launches) * (weight of left vertices)
def heur12(node, problem):

    min_vc = float('Inf')
    for i in range(node.state.depth_level, len(problem.l_list)):
        launch = problem.l_list[i]
        if launch.vc < min_vc:
            min_vc = launch.vc

    in_space = node.state.present + node.state.manifest
    w_not_launched = problem.total_weight
    for vertex in in_space:
        w_not_launched -= vertex.w

    h = min_vc * w_not_launched#se isto não funcionar, apaga

    return h    




# complex heuristic function that calculates the h cost, based on dijkstra
def heur2(node):
    h = 0
    #blabla
    return h

#combination of heur1 + heur2
def heur(node):
    h = 0
    #blabla
    return h



