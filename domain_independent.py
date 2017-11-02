from solver_library import *
from domain_dependent import *
#from utility import *

######################################################################
# general_search
#   function where is implemented the general search algorithm
#input: problem, strategy
#output: solution, cost

def general_search(problem, strategy):

    node = Node()                   # defining first node
    #node.state = 0                  # at the start, there is nothing in space
    # modifiquei a verificação do goal_check() para que isto funcionasse
    # inicialização feita dentro do expand_node()

    frontier = [node]               # list of nodes on the frontier
    explored = []                   # list of nodes explored

    n = 0

    # Main cycle
    while True:

        if not frontier: # Empty frontier - error
            solution = 'Solution not found\n'
            #soulution = ''# conforme enunciado
            cost = int(0) # force it to be a single 0
            break

        node = choose_node(frontier, strategy) # Choose node to be explored

        goal = goal_check(node.state, problem)
        #print_state(node.state)
        if goal == 1:   # achieved goal
            solution = generate_answer(node)
            break

        else:           # goal not achieved: continue exploring
            # Expand all possible nodes reachable from the current node
            frontier, explored = expand_node(frontier, explored, node, problem, strategy)
            
            #explored.append(copy.deepcopy(node))   # node has now been explored
            explored.append(node)

            if node in frontier:
                frontier.remove(node)
            '''
            print("after this node removal:")
            print_frontier(frontier)
            input()
            '''

        #if node.state.depth_level == 0:
        #    print("1.º ciclo")
        #else:
        #    print("")
        #print("depth_level =", node.state.depth_level)
        #vai adicionando aqui prints para ir fazendo debug...
        #input("keypress")#debug
        #print("------------------------------------------------------------------------")
    n = len(explored) + 1 # expanded nodes
    print('\nn =', str(n))
    print("chegou ao fim!!!\n")
    return solution
