################################################################################
# uniform_cost
#   Finds the node in the frontier with the minimum g function
# input: frontier
# output: node index on the frontier


########### como é óbvio, isto é domain dependent, só estou a usar aqui para debug...
def print_vertex_list(vertex_list):#usar para imprimir manifest e present
    print("[", end = "")
    for v in vertex_list:
        print(v.ide, end = ",")
    print("]")

def print_node(node):
    print("+++++++++++   node   ++++++++++++")
    print("  manifest = ", end = "")
    print_vertex_list(node.state.manifest)
    print()
    print("  depth =", node.state.depth_level)
    print("  date =", node.state.launch.date)
    print("  mp =", node.state.launch.mp)
    print("  fc =", node.state.launch.fc)
    print("  vc =", node.state.launch.vc)
    print("  present = ", end = "")
    print_vertex_list(node.state.present)
    print("  g =", node.g)
    print("  h =", node.h)
    print("  parent_node.manifest = ", end = "")
    print_vertex_list(node.parent_node.state.manifest)

    input("++++++++++++   end node   ++++++++++++\n")################################### INPUTTTTTTTT


def print_frontier(frontier):
    for node_f in frontier:
        print_node(node_f)
########### como é óbvio, isto é domain dependent, só estou a usar aqui para debug...




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

    print("n_node =", n_node)
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
