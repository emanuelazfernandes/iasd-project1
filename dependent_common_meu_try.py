# Python built-in libraries
import datetime
from itertools import combinations
import copy

class Vertex:

    def __init__(self):
        self.w = float(0)               # Module weight
        self.c = []              # List of modules which connect to this module
        self.ide = ''            # Module identification - name/string

class Launch:

    def __init__(self):
        self.date = []                # Date of the launch
        self.mp = 0                   # Maximum payload of the launch
        self.fc = 0                   # Fixed cost of the launch
        self.vc = 0                   # Variable cost of the launch

class Node:

    def __init__(self):
        self.state = State()        # Node state
        self.g = 0                  # Path cost from the first node
        self.h = 0                  # Heuristic function
        self.parent_node = None     # Node that originated this one

class State:

    def __init__(self):
        self.present = []            # list of vertices present in space
        self.manifest = []           # list of vertices that are going in this launch

        self.depth_level = 0
        self.launch = Launch() # arranja maneira de meter cada node.state com um unico launch! acho que é mais fácil assim
        #self.launches = []           # list of past launch dates
        # Auxiliary variables for heuristic calculation
        #self.reached_goal_stack = False
        #self.return2stack = False

class Problem:
    #initial_state = 0               # First Node state - 0 vertex in space
    l_list = None                   # List of scheduled launches
    v_list = None                   # List of Modules to launch
    goal_state = 0                  # Number of vertices in space


###############################################################################
# reorder_dat
#   Will reorder the initial file: first the Cask lines, then the Stack lines,
# and finaly, the Edge lines.. This way, the entries in the input file can
# appear in any order.
# Input: file_name
# Output: list of strings with each line type ordered (Casks then Stacks then
#edges)

def order_file(file_name):

    with open(file_name) as f:
        # "mini-files", each has only one time of line, eg. s_line on has the
        #stack lines of the original file
        v_file = []
        e_file = []
        l_file = []

        # stores each mini-file
        for line in f:

            if line[0] == 'V':
                v_file.append(line)
            elif line[0] == 'E':
                e_file.append(line)
            elif line[0] == 'L':
                l_file.append(line)

    # writes the new file
    ordered_file = []
    for line in v_file:
        ordered_file.append(line)
    for line in l_file:
        ordered_file.append(line)
    for line in e_file:
        ordered_file.append(line)

    return ordered_file


###############################################################################
# read_file
# Function that reads the input file and defines the problem
# Input: file_name
# Output: problem

def read_file(file_name):
    v_list = []     # list of modules (Vertex) with the info of each module
    l_list = []     # list of launches (Launch)

    # gets ordered version of the input file
    ordered_file = order_file(file_name)

    for line in ordered_file:

        # removes '\n' character
        line = line.rstrip()
        # splits every word in the line separated by whitespace
        words = line.split()

        if line[0] == 'V':
            # initializes the Vertex class
            v = Vertex()
            v.ide = words[0]
            v.w = float(words[1])
            # adds it to the cask list
            v_list.append(v)
            #adicionar aqui verificações extra (repetições, etc)...

        elif line[0] == 'E':
            # adds connections to the respective Vertex classes
            for v in v_list:
                if v.ide == words[1]:
                    v.c.append(words[2])
                elif v.ide == words[2]:
                    v.c.append(words[1])
            #adicionar aqui verificações extra (repetições, etc)...

        elif line[0] == 'L':
            # initializes the Launch class
            l = Launch()
            l.date = datetime.date(int(words[1][4:8]), int(words[1][2:4]), int(words[1][0:2]))
            l.mp = float(words[2])
            l.fc = float(words[3])
            l.vc = float(words[4])
            # adds it to the cask list
            l_list.append(l)
            #adicionar aqui verificações extra (repetições, etc)...


    # orders launch list by date
    l_list = sorted(l_list, key=lambda item: item.date)

    # initializes our Problem
    problem = Problem()
    #problem.initial_state = 0 #estava comentado lá em cima.....
    problem.v_list = v_list
    problem.l_list = l_list
    problem.goal_state = len(v_list) # goal state is the number of vertices in space
    #leva isto depois em consideração, para ele não adicionar quando estiver a explorar o node que não envia nada...

    #debug - depois apaga/comenta
    print("vertex w c")
    for v in v_list:
        print(v.ide, v.w, v.c)
    print("\nlaunch: date mp fc vc")
    for l in l_list:
        print(l.date, l.mp, l.fc, l.vc)
    print("\nproblem:")
    #print(problem.initial_state, problem.goal_state)# initial_state comentado lá em cima.....
    print(problem.goal_state)
    print()


    return problem

###############################################################################
# choose_node
#   choose node to be expanded next according to strategy
# Input: frontier, strategy
# Output: node - to be expanded next

def choose_node(frontier, strategy):

    n_node = strategy['search'](frontier) # n_node: node position on frontier

    node = frontier[n_node]

    return node

###############################################################################
# goal_check
#   function that checks if goal is achieved
# Input: state, problem
# Output: goal - 1 if achieved, 0 if not

def goal_check(state, problem):

    goal = 0
    if len(state.present) == problem.goal_state:
        goal = 1 # Every component in orbit!
        #adiciona aqui checks adicionais...

    return goal

###############################################################################
# generate_answer
#   When the goal is found, the function writes the sequence of actions and cost
# Input: node - goal node
# Output: solution, cost

def generate_answer(node):

    s = '' # solution string
    cost = node.g # Total cost
    mother_cost = cost

    ###gera output, falta fazer
    ## ok - é preciso percorrer agora o visited pela ordem correcta através dos
    # node_mother, para fazer o backtrace e obter o caminho óptimo..
    # depois inverter essa ordem e ir imprimindo o que é necessário no s,
    # conforme o enunciado e os outputs do prof

    return s, cost


###############################################################################
# expand_node
#   Expands all the possible nodes that are reachable from the current node.
# Essential part of the program, taking into consideration all the constraints.
# Only expands a certain node if is not on the frontier and explored list and,
# in the case it is on the frontier list, chooses the one with the lowest cost.
# Input: frontier, explored, node_mother, problem, strategy
# Output: frontier, explored

def expand_node_emanuel(frontier, explored, node_mother, problem, strategy):

    if not node_mother.parent_node: # quer dizer que é o primeiro
        # inicializar o node_mother:
        node_mother.state.launch = problem.l_list[0]

    vertex_tl = problem.v_list # aqui não será preciso fazer deepcopy?
    #launch_av = problem.l_list # aqui não será preciso fazer deepcopy?
    search = strategy['search']         # search algorithm to be implemented


    ## consider only launches that have not happened, and if a launch has happened ignore launches previous to that one
    #for launch in problem.l_list:
    #    if launch in node_mother.state.launches:
    #        launch_av.remove(launch)#esperemos que ele aqui só remova deste local =X
    #    if launch < max(node_mother.state.launch.date):
    #        launch_av.remove(launch)#esperemos que ele aqui só remova deste local =X
    # we now have a list of the launches we have available

    # ele vai sempre escolher o 1.º, por isso acho que isto pode ser feito de melhor maneira...
    # a minha sugestão é ir incrementando um contador de depth/nível,
    # apagar a lista de launches do state e deixar só um launch por node,
    # sendo que usamos esse contador para escolher o launch do problem.l_list

    # consider only unlaunched vertices/components
    for vertex in problem.v_list:
        if vertex in node_mother.state.present: # if vertex in space, it cant be launched
            vertex_tl.remove(vertex)#esperemos que ele aqui só remova deste local =X

        # list of the eligible vertex to launch
        # if vertex.c not in con_list:
        #    con_list = con_list.append(vertex.c)
        # acho que isto aqui fica melhor com as funções que já tinha feito - não são bonitas mas funcionam =(

    # list with possible, launchable vertex
    # for vertex in v_list:
    #    if vertex.ide not in con_list:
    #        v_list.remove(vertex)
    # acho que já fiz isto tudo que querias


    # generate all the possible combinations of components to launch
    con_list = generate_combinations(vertex_tl)

    # apply edges filter
    filter_edges(con_list, vertex_tl)

    #apply weight filter
    filter_weight(con_list, node_mother.state.launch.mp)

    # add new created nodes to frontier
    frontier_add_nodes(frontier, con_list, node_mother, vertex_tl, problem)

    # teoricamente, o explored aqui não é modificado...

    return frontier, explored




# FUNÇÕES ADICIONADAS POR MIM - EMANUEL

# aux function to generate all of the possible launch components combinations
def generate_combinations_emanuel(v_list):

    #aqui somos obrigados a fazer isto assim por causa do combinations e sum_w
    list_V = {} # aux dict
    for v in v_list:
        list_V[v.ide] = v.w
        #{'VCM' = 20.4, 'VDM' = ...}
    list_comb = []

    #print("possible combinations: ")#debug
    for k in range(0, list_V.__len__()+1):
        #print(k, end = ': ')#debug
        comb_aux = list(combinations(list_V.keys(), k))
        for j in range(0, len(comb_aux)): # format it for single list
            sum_weights = float(0)
            for c in comb_aux[j]:
                sum_weights += list_V[c]#sum the weights of the combination, DEIXA FICAR O V, POIS É O DICT ORIGINAL

            list_comb.append((comb_aux[j], sum_weights))
        #print(comb_aux)#debug
        #print(comb_aux.__len__())#debug
        #print()#debug

    #print()#debug
    #print(list_comb)#debug

    return list_comb


# function that filters the combinations generated, if at least 1 element
# will be unconnected in orbit, except the first one
def filter_edges_emanuel(list_comb, v_list):

    # create aux dict for edges
    list_E_aux = {}
    for v in v_list:
        list_E_aux[v.ide] = v.c

    prev_size = len(list_comb)
    n_rem = 0#debug
    for cln in reversed(range(0, prev_size)):
        comp_manifest = list_comb[cln][0]

        if len(comp_manifest) <= 1: # remove all but first
            continue
        not_edge = True # flag to find edges
        for comp_aux_n in range(0, len(comp_manifest)):

            comp_aux = comp_manifest[comp_aux_n]

            for next_comp in comp_manifest[:comp_aux_n]+comp_manifest[comp_aux_n+1:]:
                if next_comp in list_E_aux[comp_aux]:
                    not_edge = False
                    break # if found, activate flag and break (save cycles)

            if not_edge:# found one that's not connected to any of the others
                break # save cycles
        
        if not_edge:
            n_rem = n_rem + 1#debug
            del(list_comb[cln])

    #print("\nTotal invalid combinations removed:",n_rem,"out of",prev_size,"\n")#debug


#function that filters list_comb based on available weight
def filter_weight_emanuel(list_comb, launch_weight):
    for cwn in reversed(range(0,len(list_comb))):
        if list_comb[cwn][1] >= launch_weight:
            del(list_comb[cwn])
    print(list_comb)#debug
    print()#debug


def frontier_add_nodes_emanuel(frontier, list_comb, node_mother, v_list, problem):

    for c in list_comb: # c = ('manifest', sum_weight)
        node_aux = Node()
        state_aux = State()

        # populate state
        state_aux.present = node_mother.state.present # list of vertices present in space
        for pc in node_mother.state.manifest:# now with the parent ones!
            state_aux.present.append(pc)#vê lá se isto não adiciona aos da mãe também.....

        for v in v_list:
            if v.ide in c[0]:
                state_aux.manifest.append(v)

        state_aux.depth_level = node_mother.state.depth_level + 1
        state_aux.launch = problem.l_list[state_aux.depth_level-1]

        # populate node
        node_aux.state = state_aux
        node_aux.g = calculate_cost(state_aux.launch, state_aux.manifest, c[1])
        node_aux.h = 0 #depois: node_aux.h = from_heuristic()
        node_aux.parent_node = node_mother

        frontier.append(node_aux)


# function that calculates launch cost
def calculate_cost_emanuel(launch, manifest, sum_w):

    sum_c = float(0)
    if manifest: #só entra aqui se tiver pelo menos 1! - verifica que funciona..
        sum_c = launch.fc + launch.vc*sum_w

    return sum_c


########################################################################################################################
def expand_node(frontier, explored, node_mother, problem, strategy):

    if not node_mother.parent_node: # quer dizer que é o primeiro
        # inicializar o node_mother:
        node_mother.state.launch = problem.l_list[0]

    vertex_tl = problem.v_list # aqui não será preciso fazer deepcopy?

    search = strategy['search']         # search algorithm to be implemented




    # consider only unlaunched vertices/components
    for vertex in problem.v_list:
        if vertex in node_mother.state.present: # if vertex in space, it cant be launched
            vertex_tl.remove(vertex)#esperemos que ele aqui só remova deste local =X




    # generate all the possible combinations of components to launch
    combi_list = generate_combinations([],vertex_tl,[])

    #still have to generate the empty payload combination





    combi_list= filter_weight(combi_list, node_mother.state.launch.mp)

    con_list = []
    # apply weight filter
    for combb in combi_list:
        for vertice in combb:
            combinacao=[]
            combinacao.append(vertice)
            con_list.append(combinacao)


    # apply edges filter
    #filter_edges(combi_list, node_mother)



    # add new created nodes to frontier
    frontier_add_nodes_emanuel(frontier, con_list, node_mother,vertex_tl, problem)

    # teoricamente, o explored aqui não é modificado...

    return frontier, explored

########################################################################################################################

def generate_combinations(target,data,all_combinations):

    for i in range(len(data)):
        new_target = copy.copy(target)
        new_data = copy.copy(data)
        new_target.append(data[i])
        new_data =data[i+1:]
        all_combinations.append(new_target)
        generate_combinations(new_target, new_data, all_combinations)

    return all_combinations

########################################################################################################################




def filter_edges(combi_list,node_mother):
    connect_list=[]
    for vertex in node_mother.state.present:
        if not node_mother.state.present:
            break

        for connec in vertex.c:
            print("connec")
            if connec not in connect_list:
                connect_list.append(connec)
                print("o")


#    for combination in combi_list:
#        print("i")
#        for vertex2 in combination:
#            for connecti in vertex2.c:
#                if connecti not in connect_list:
#                    print("a")
#                    combi_list.remove(combination)
#                    continue
#            continue
#        continue


 #   for combination in combi_list:
 #       print(type(combination[0]))

#    for i in range(0,len(combi_list)):
#        print(type(combination))
#        for vertex3 in range(0, len(combi_list(combination))):
#            if vertex3 not in connect_list:
#                combi_list.remove(combi_list(combination))
    combi_list = combi_list[:(len(combi_list)//2) - 1]

    return combi_list

########################################################################################################################

def filter_weight(combi_list,launch_weight):

    combi_weight=float(0)
    for combination in combi_list:
        for vertex in combination:
            combi_weight+=vertex.w

        if combi_weight>launch_weight:
            combi_list.remove(combination)

    return combi_list

########################################################################################################################

def frontier_add_nodes(frontier, combi_list, node_mother, problem):

    for combi in combi_list:
        print("i")
        combi_weight = float(0)
        node_aux = Node()


        node_aux.state.present=node_mother.state.present

        for vertex in node_mother.state.manifest:
            node_aux.state.present.append(vertex)

        node_aux.manifest=combi

        node_aux.state.depth_level=node_mother.state.depth_level + 1
        print(node_aux.state.depth_level)

        node_aux.state.launch=problem.l_list[node_mother.state.depth_level]

        for module in node_aux.manifest:
            combi_weight += module.w

        node_aux.g = calculate_cost(node_aux.state.launch, node_aux.state.manifest, combi_weight)
        node_aux.h = 0  # depois: node_aux.h = from_heuristic()
        node_aux.parent_node = node_mother

        print(len(frontier))

        frontier.append(node_aux)

########################################################################################################################

def calculate_cost(launch, manifest, launch_sum_w):

    cost = float(0)
    if manifest: #só entra aqui se tiver pelo menos 1! - verifica que funciona..
        cost = launch.fc + launch.vc*launch_sum_w

    return cost
