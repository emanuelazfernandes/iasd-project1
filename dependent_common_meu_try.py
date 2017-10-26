# Python built-in libraries
import sys
import datetime
from itertools import combinations

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
    #print("\nproblem:")
    #print(problem.initial_state, problem.goal_state)# initial_state comentado lá em cima.....
    #print(problem.goal_state)
    #print()


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




def expand_node(frontier, explored, node_mother, problem, strategy):

    if not node_mother.parent_node: # quer dizer que é o primeiro
        # inicializar o node_mother:
        node_mother.state.launch = problem.l_list[0]

    print("MOTHER NODE")
    print("Vertex in Space ", end="")

    for vert1 in node_mother.state.present:
        print(" ",vert1.ide, end="")

    print("")
    print("Cost ",node_mother.g)

    print("Vertex to Launch ")
    for vert2 in node_mother.state.manifest:
        print(" ", vert2.ide, end="")








    vertex_tl = problem.v_list # aqui não será preciso fazer deepcopy?
    #launch_av = problem.l_list # aqui não será preciso fazer deepcopy?
    search = strategy['search']         # search algorithm to be implemented


    # consider only unlaunched vertices/components
    for vertex in problem.v_list:
        if vertex in node_mother.state.present: # if vertex in space, it cant be launched
            vertex_tl.remove(vertex)#esperemos que ele aqui só remova deste local =X



    con_list = generate_combinations(vertex_tl)
    #print("comb before filter")
    #print(len(con_list))

    con_list=filter_launched(con_list,node_mother,problem)

    #apply weight filter
    filter_weight(con_list, node_mother.state.launch.mp)
    #print("after weight filter")
    #print(len(con_list))

    con_list=filter_edges(con_list,node_mother,problem)
    #print("after edge filter")
    #print(len(con_list))


    # add new created nodes to frontier
    frontier_add_nodes(frontier, con_list, node_mother, vertex_tl, problem)

    # teoricamente, o explored aqui não é modificado...

    return frontier, explored




# FUNÇÕES ADICIONADAS POR MIM - EMANUEL

# aux function to generate all of the possible launch components combinations
def generate_combinations(v_list):

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


def filter_launched(list_comb,node_mother,problem):

    space_vert=[]
    for vert in node_mother.state.present:
        space_vert.append(vert.ide)

    possible_vertex=[]
    for verte in problem.v_list:
        if verte.ide not in space_vert:
            possible_vertex.append(verte.ide)


    new_list=[]
    for tuple_comb in list_comb:
        for vert_str in tuple_comb[0]:
            if vert_str in possible_vertex:
                new_list.append(tuple_comb)

        break

    return new_list


def filter_edges(list_comb,node_mother,problem):

    possible_vertex=[]
    if not node_mother.state.present:
        for vertex in problem.v_list:
            possible_vertex.append(vertex.ide)


    for vertex in node_mother.state.present:
        for conn in vertex.c:
            if conn not in possible_vertex:
                possible_vertex.append(conn)

    print("possible vert ",possible_vertex)

    new_list=[]
    for tuple_comb in list_comb:
        for vert_str in tuple_comb[0]:
            if vert_str in possible_vertex:
                new_list.append(tuple_comb)

        break

    return new_list



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
def filter_weight(list_comb, launch_weight):
    for cwn in reversed(range(0,len(list_comb))):
        if list_comb[cwn][1] >= launch_weight:
            del(list_comb[cwn])
    #print(list_comb)#debug
    print()#debug


def frontier_add_nodes(frontier, list_comb, node_mother, v_list, problem):

    for c in list_comb: # c = ('manifest', sum_weight)
        node_aux = Node()
        state_aux = State()

        # populate state
        state_aux.present = node_mother.state.present # list of vertices present in space
        for pc in node_mother.state.manifest:# now with the parent ones!
            if pc not in state_aux.present:
                state_aux.present.append(pc)#vê lá se isto não adiciona aos da mãe também.....

        for v in v_list:
            if v.ide in c[0]:
                if v not in state_aux.manifest:
                    state_aux.manifest.append(v)

        state_aux.depth_level = node_mother.state.depth_level + 1
        state_aux.launch = problem.l_list[state_aux.depth_level-1]

        # populate node
        node_aux.state = state_aux
        node_aux.g = node_mother.g + calculate_cost(state_aux.launch, state_aux.manifest, c[1])
        node_aux.h = 0 #depois: node_aux.h = from_heuristic()
        node_aux.parent_node = node_mother

        frontier.append(node_aux)


# function that calculates launch cost
def calculate_cost(launch, manifest, sum_w):

    sum_c = float(0)
    #if manifest: #só entra aqui se tiver pelo menos 1! - verifica que funciona..
    sum_c = launch.fc + launch.vc*sum_w

    return sum_c
