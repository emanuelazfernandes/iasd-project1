# Python built-in libraries
import sys
import datetime
import copy
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
    l_aux = Launch()
    l_aux.date = datetime.date(int(9999), int(12), int(31))
    ordered_file = order_file(file_name)
    l_list.append(l_aux)
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
    if len(state.present)+len(state.manifest) == problem.goal_state:
        goal = 1 # Every component in orbit!
        #adiciona aqui checks adicionais...
        print("@ goal")
        print_state(state)
    return goal

###############################################################################
# generate_answer
#   When the goal is found, the function writes the sequence of actions and cost
# Input: node - goal node
# Output: solution, cost

def generate_answer(node):

    output = []

    print("\ngenerate_answer()")

    node_print = node

    output.append('{0:.6f}'.format(node_print.g))

    while node_print.parent_node:
        cost_node = node_print.g - node_print.parent_node.g
        if cost_node != 0:
            s = ''
            s += node_print.state.launch.date.strftime("%d%m%Y")
            s += " "*3
            for v in node_print.state.manifest:
                s += v.ide + " "
            s += " "*2
            s += str('{0:.6f}'.format(cost_node))
            output.append(s)
        #else:
        #    output.append("(envio vazio)")
        node_print = node_print.parent_node
        #print("---------")

    return '\n'.join(reversed(output))



def expand_node(frontier, explored, node_mother, problem, strategy):

    if not node_mother.parent_node: # quer dizer que é o primeiro
        # inicializar o node_mother:
        #node_mother.state.launch = copy.deepcopy(problem.l_list[0])
        node_mother.state.launch = problem.l_list[0]

    #print("-----------------------------------------")
    #node_print=copy.deepcopy(node_mother)
    #while node_print.parent_node:
        #print("MOTHER NODE")
        #print("Vertex in Space - ", end="")
        #for vert1 in node_print.state.present:
        #    print(" ",vert1.ide, end="")
        #print("")
        #print("Cost - ",node_print.g)
        #print("Vertex to Launch - ",end="")
        #for vert2 in node_print.state.manifest:
        #    print(" ", vert2.ide, end="")
        #print("")
        #print("Launch - ", node_print.state.launch.date,  node_print.state.launch.mp)
        #print("Depth - ",node_print.state.depth_level)
        #node_print=copy.deepcopy(node_print.parent_node)
        #print("---------")
    #print("-----------------------------------------")
    #print("")
    #print("")
    #print("")
    #print("Launch - ", problem.l_list[node_mother.state.depth_level].date, problem.l_list[node_mother.state.depth_level].mp)
    vertex_tl = copy.deepcopy(problem.v_list)# aqui ele precisa MESMO do deepcopy...
    #launch_av = problem.l_list # aqui não será preciso fazer deepcopy?
    search = strategy['search']         # search algorithm to be implemented

    vertex_tl = filter_launched(vertex_tl, node_mother)
    #print("after launched filter - ",len(vertex_tl))
    #for vert2 in vertex_tl:
    #    print(" ", vert2.ide, end="")
    #print(" ")
    
    vertex_tl = filter_manifest(vertex_tl, node_mother)
    #print("after manifest filter - ",len(vertex_tl))
    #for vert2 in vertex_tl:
    #    print(" ", vert2.ide, end="")
    #print(" ")



    #vertex_tl = filter_edges(vertex_tl, node_mother, problem)####################################################
    #for vert2 in vertex_tl:
    #    print(" ", vert2.ide, end="")
    #print(" ")

    #con_list = generate_combinations(vertex_tl)
    con_list = generate_combinations(vertex_tl, node_mother.state.present, problem)
    
    con_list = filter_weight(con_list, problem.l_list[node_mother.state.depth_level].mp)
    #print("after weight filter - ",len(con_list))


    #print(problem.l_list[node_mother.state.depth_level].mp)
    #for comb in con_list:
    #    print(" ", comb, end="")
    '''
    for comb in con_list:
        if comb[1] == 0:
            con_list.remove(comb)
    '''
    ########################con_list = filter_combinations(con_list, vertex_tl, node_mother, problem)

    '''
    print("node_g =", node_mother.g, end = ", ")
    print("manifest =", end = "[")
    for v in node_mother.state.manifest:
        print(v.ide, end = ",")
    print("]")
    print("node_depth =", node_mother.state.depth_level)
    print("before add_nodes():")
    print_frontier(frontier)
    '''
    # add new created nodes to frontier
    frontier_add_nodes(frontier, explored, con_list, node_mother,  problem)
    '''
    print("after add_nodes(), but before this node removal:")
    print_frontier(frontier)
    '''
    

    return frontier, explored




# FUNÇÕES ADICIONADAS POR MIM - EMANUEL

# aux function to generate all of the possible launch components combinations
def generate_combinations(v_list, present, problem):
    list_V = {} # aux dict: #{'VCM' = 20.4, 'VDM' = ...}
    for v in v_list:
        list_V[v.ide] = v.w

    list_comb = []
    list_comb.append(([],0))# adicionamos manualmente o lançamento vazio

    if present:
        print("not yet (for present)")
        input()
    else:
        for v in v_list:
            aux = [v.ide]
            #for k in range(1, len(problem.v_list)+1):
            aux2 = copy.copy(aux)
            list_circles = find_circles(aux2, problem)#pode retornar 3, 4 ou 5 circles
            #print("k =", k)
            print("aux2 =", aux2, "list_circles =", list_circles)
            input()



                #for circle in list_circles:


                #aux2.extend()
            #


    #geras a combinação (já tem de ser correcta)
    #verificas se já existe
    #se não, então adiciona à lista de combinações

    return list_comb




def find_circles(aux, problem):#aux = ['CM'], ou aux = ['CM','K1'], ou aux = ['CM','K1','K']
    list_circles = []# uma lista com os vertex de cada circle, formato: [['CM','K1'],['PM',STM','P','K','K2','S'],['DM']]
    
    inner = copy.copy(aux)#talvez copy ou deepcopy?
    explored = []
    outer = find_outer(inner, problem, explored)
    #print("inicial inner =", inner)
    #print("inicial outer =", outer)

    explored.extend(inner)
    list_circles.append(inner)
    #print("inicial list_circles =", list_circles)
    while outer:
        inner = copy.copy(outer)#talvez copy ou deepcopy?
        print("entrou outer =", outer)
        outer = find_outer(inner, problem, explored)
        print("saiu outer =", outer)
        input()

        explored.extend(inner)
        list_circles.append(inner)
        #print("list_circles =", list_circles)
        #input()

    return list_circles

def find_outer(inner, problem, explored):#inner_start = aux
    outer = []
    #print("inner =", inner)
    for v_in in inner:#v_in = 'CM'; v_in = 'K1'
        edges = return_edges(problem, v_in)#edges = ['K1','STM','P','K','K2','S']; edges = ['PM','CM']
        #print("v_in =", v_in, '| edges =', edges)
        foundit = False#poupar ciclos; mas nao sei se isto funciona na mesma com isto...
        for e in edges:#e = 'K1'
            #for a in inner:#a = 'CM'; a = 'K1' !
            for a in explored:
                if e == a:
                    edges.remove(e)#remover edges que contenham um dos outros aux
                    foundit = True#poupar ciclos; mas nao sei se isto funciona na mesma com isto...
                    break#poupar ciclos; mas nao sei se isto funciona na mesma com isto...
            if foundit:#poupar ciclos; mas nao sei se isto funciona na mesma com isto...
                break#poupar ciclos; mas nao sei se isto funciona na mesma com isto...
        #edges = ['STM','P','K','K2','S']; edges = ['PM']
        #print("after testit: edges =", edges)

        outer.extend(edges)#outer = ['STM','P','K','K2','S']; outer = ['STM','P','K','K2','S','PM']
        #print("outer =", outer)
        #input()
    print("outer =", outer)
    input()
    return outer

def return_edges(problem, vertex_str):#vertex_str = 'VDM'
    for ve in problem.v_list:#vamos ver agora todos os vizinhos do 'VDM'
        if ve.ide == vertex_str:
            edges = ve.c#edges tem agora uma lista de string com os vizinhos de VDM: ['VK']
            break#já encontramos; poupar ciclos
    return edges











def filter_manifest(vertex_tl, node_mother):

    possible_vertex = []

    for verr in node_mother.state.manifest:
        for verte in vertex_tl:
            if verr.ide == verte.ide:
                vertex_tl.remove(verte)

    return vertex_tl


def filter_launched(vertex_tl, node_mother):

    for verr in node_mother.state.present:
        for verte in vertex_tl:
            if verr.ide == verte.ide:
                vertex_tl.remove(verte)

    return vertex_tl


def filter_edges(vertex_tl, node_mother, problem):

    possible_vertex_conn_str = []

    vertex_in_space = node_mother.state.present + node_mother.state.manifest

    for vertex in vertex_in_space:
        for conn in vertex.c:
            if conn not in possible_vertex_conn_str:
                possible_vertex_conn_str.append(conn)

    if not vertex_in_space:
        possible_vertex_conn_str = []
        for vertex in problem.v_list:
            possible_vertex_conn_str.append(vertex.ide)

    possible_vertex = []

    for vertex in vertex_tl:
        if vertex.ide in possible_vertex_conn_str:
            possible_vertex.append(vertex)

    unconected_list = []
    for vertex in problem.v_list:
        unconected_list.append(vertex)

    for vert in possible_vertex:
        for verr in unconected_list:
            if vert == verr:
                unconected_list.remove(vert)

    return possible_vertex


#function that filters list_comb based on available weight
def filter_weight(list_comb, launch_weight):
    for cwn in reversed(range(0,len(list_comb))):
        if list_comb[cwn][1] >= launch_weight:
            del(list_comb[cwn])
    #print(list_comb)#debug
    #print()#debug
    return(list_comb)

'''
def filter_combinations(con_list, vertex_tl, node_mother, problem):

    outer_ring = []

    for c_tup in con_list:
        #c_tup = (['VK1','VS','VSTM'],6.9)
        comb = c_tup[0]
        #comb tem agora a lista de strings desta combinação => ['VK1','VS','VSTM']
        if len(comb) < 2:
            continue#só estamos interessados em eliminar aqueles que têm pelo menos 2 componentes, pois o objectivo aqui é verificar se vão ficar conectados no espaço...
        for n_vide in range(0, len(comb)):
            vide = comb[n_vide]
            #vide contem agora o v.ide da comb => 'VK1'
            for v_orig in problem.v_list#procurar os edges do VK1
                if v_orig.ide == vide:
                    edges = v_orig.c
            #edges contem agora ['VPM','VCM'], uma lista de strings!!!
            comb_others = comb[:n_vide] + comb[n_vide+1:]
            #comb_others contem agora todos os outros da comb que não o vide => ['VS','VSTM']

            for co in comb_others:
                if co not in edges:
                    blabla
'''
    #percorrer as combinações 1 por 1, e ver se há pelo menos 1 desconexão!
    #se houver, essa combinação salta fora!


'''
    print(con_list)

    possible_vertex_conn_str = []

    vertex_in_space = node_mother.state.present + node_mother.state.manifest
    for v in vertex_in_space:
        print("     ", v.ide, end = "")
    print("caralho")

    for vertex in vertex_in_space:
        for conn in vertex.c:
            if conn not in possible_vertex_conn_str:
                possible_vertex_conn_str.append(conn)
    print(possible_vertex_conn_str)

    if not vertex_in_space:
        possible_vertex_conn_str=[]
        for vertex in problem.v_list:
            possible_vertex_conn_str.append(vertex.ide)
    print(possible_vertex_conn_str)

    for combi in con_list:
        if len(combi[0])==1:
            if combi[0] not in possible_vertex_conn_str:
                con_list.remove(combi)
    print(con_list)
    input()
    #até aqui, já filtrou .....

    #for 

    return con_list
'''

def frontier_add_nodes(frontier, explored, list_comb, node_mother, problem):

    for c in list_comb: # c = ('manifest', sum_weight)
        node_aux = Node()
        state_aux = State()

        # populate state
        state_aux.present = copy.deepcopy(node_mother.state.present)# aqui ele precisa MESMO do deepcopy...
        for pc in node_mother.state.manifest:# now with the parent one
            if pc not in state_aux.present:
                state_aux.present.append(pc)#vê lá se isto não adiciona aos da mãe também.....

#        for v in problem.v_list:
#            if v.ide in c[0]:
#                if v not in state_aux.manifest:
#                    if c[1] != 0:
#                        if v not in node_mother.state.present:
#                            state_aux.manifest.append(v)

        for vert_name in c[0]:
            for  verr in problem.v_list:
                if verr.ide==vert_name:
                    #print("a")
                    if verr not in node_mother.state.manifest:
                        #print("b")
                        state_aux.manifest.append(verr)

        state_aux.depth_level = node_mother.state.depth_level + 1
        state_aux.launch = problem.l_list[state_aux.depth_level-1]

        #print("state_aux.depth_level = ", state_aux.depth_level)
        #print("node_mother.state.depth_level = ",node_mother.state.depth_level)


        # populate node
        node_aux.state = state_aux
        node_aux.g = node_mother.g + calculate_cost(state_aux.launch, state_aux.manifest, c[1])

        node_aux.h = 0 #depois: node_aux.h = from_heuristic()
        #node_aux.parent_node = copy.deepcopy(node_mother)
        node_aux.parent_node = node_mother

        '''
        #check if node is already in explored
        if not in_explored(node_aux, explored):
            frontier.append(node_aux)
        else:#debug
            print("node já presente:")#debug
            for ne in explored:
                if set(node1.state.manifest) == set(node2.state.manifest) and \
                    set(node1.state.present) == set(node2.state.present) and \
                    node1.state.manifest and node2.state.manifest:
        '''
        # se calhar isto aqui em cima nem é necessário...
        frontier.append(node_aux)


# function that calculates launch cost
def calculate_cost(launch, manifest, sum_w):

    if manifest:
        sum_c = launch.fc + launch.vc*sum_w
    else:
        sum_c = 0

    return sum_c


#print the combinations list
def print_comb(list_comb):
    print("List of combinations = {")
    print("  n\tsum_w\tlist_components")
    print("-----------------------------------------")
    for pcn in range(0,list_comb.__len__()):
        print(" ",pcn,end = "")
        print(":\t",end="")
        print("{0:.2f}".format(list_comb[pcn][1]),end = "\t")
        print(list_comb[pcn][0])
    print("} size =",list_comb.__len__(),"\n")

def print_state(state):
    print("node.state:")
    print("present = [",end = "")
    for vp in state.present:
        print(vp.ide+",", end = "")
    print("]")
    print("manifest = [",end = "")
    for vm in state.manifest:
        print(vm.ide+",", end = "")
    print("]")
    print("depth =", state.depth_level)
    print("date =", state.launch.date)
    print()



def print_frontier(frontier):
    print("           frontier = { ", end = "")
    for nf in frontier:
        print("(", end = "")
        print(str(nf.g) + ",", end = "")
        print("[", end = "")
        for vm in nf.state.manifest:
            print(vm.ide + ",", end = "")
        print("]", end = "")
        print("[", end = "")
        for vp in nf.state.present:
            print(vp.ide + ",", end = "")
        print("]", nf.state.depth_level, end = "")
        print("), ", end = "")
    print("}")




def in_explored(node_aux, explored):
    already_explored = False

    for ne in explored:
        if equal_nodes(node_aux, ne):
            already_explored = True

    return already_explored



def equal_nodes(node1, node2):
    are_equal = False

    if set(node1.state.manifest) == set(node2.state.manifest) and \
        set(node1.state.present) == set(node2.state.present) and \
        node1.state.manifest and node2.state.manifest:
        are_equal = True

    return are_equal

'''
    for vm1 in node1.state.manifest:
        if vm1.ide not in node2.state.manifest:
            return False

    for vp1 in node1.state.present:
        if vp1.ide not in node2.state.present:
            return False
'''
