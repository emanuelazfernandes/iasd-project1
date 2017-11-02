# Python built-in libraries
import sys
import datetime
import copy
from itertools import combinations
from solver_library import *

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
    total_weight = 0
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
    sum_w = float(0)
    for vertex in v_list:
        sum_w += vertex.w
    problem.total_weight = sum_w
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
    #vertex_tl = copy.deepcopy(problem.v_list)# aqui ele precisa MESMO do deepcopy...
    vertex_tl = copy.copy(problem.v_list)# aqui ele precisa MESMO do deepcopy...
    #launch_av = problem.l_list # aqui não será preciso fazer deepcopy?
    search = strategy['search']         # search algorithm to be implemented

    vertex_tl = filter_launched(vertex_tl, node_mother)
    
    vertex_tl = filter_manifest(vertex_tl, node_mother)



    #vertex_tl = filter_edges(vertex_tl, node_mother, problem)############################

    #con_list = generate_combinations(vertex_tl)
    con_list = generate_combinations(vertex_tl, node_mother.state.present, problem)
    
    con_list = filter_weight(con_list, problem.l_list[node_mother.state.depth_level].mp)
    #print("after weight filter - ",len(con_list))

    #print(problem.l_list[node_mother.state.depth_level].mp)
    
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
    frontier_add_nodes(frontier, explored, con_list, node_mother, problem, strategy)
    '''
    print("after add_nodes(), but before this node removal:")
    print_frontier(frontier)
    '''
    

    return frontier, explored


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#ANTIGA FUNÇÃO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
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
'''
#ANTIGA FUNÇÃO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







##############################################################################################
##################       FIM DO NOVO generate_combinations()      ############################
##############################################################################################





# aux function to generate all of the possible launch components combinations
def generate_combinations(v_list, present, problem):

    list_V = {} # aux dict: #{'VCM' = 20.4, 'VDM' = ...}
    for v in v_list:
        list_V[v.ide] = v.w

    list_comb = []
    list_comb.append(([],0))# adicionamos manualmente o lançamento vazio


    if present:
        #fazer agora o mesmo, mas usando os que já estao no present, e no fim retirar isso de cada comb gerada com eles (E O PESO!!!)
        #for vp in present:
        #    vp_ide = vp.ide
        print("not yet (for present)!")

    else:
        #sem nada lá em cima
        for v in v_list:
            #gerar todas as combinações para este vertex (v.ide = 'VDM'), enquanto houver edges não explorados!
            aux = [v.ide]
            edges = return_edges(problem, v.ide)
            #percorrer agora o edges para gerar todas as combinações 2 a 2 com esse(s), 1 a 1, 3 a 3, etc...
            for k in range(1, len(problem.v_list)+1):#como não está la nada, usamos aqui o problem.v_list; depois para o outro caso, usar só o v_list, pois já só contem a quantidade de vertex que podem ser lançados, (acho que) não precisamos de andar a gerar cenas a mais

                if k == 1:#fazer para 1 a 1
                    comb = [v.ide]#comb = ['VDM']
                    sum_w = list_V[v.ide]#sum_w = 4.3
                    comb_tup = (comb, sum_w)#comb_tup = (['VDM'],4.3)
                    list_comb.append(comb_tup)
                    #print_comb(list_comb)
                    #print("k =",k)
                    #input()

                if k == 2:#fazer para 2 a 2
                    for edge in edges:#edge = 'VK'
                        comb = [v.ide, edge]#comb = ['VDM','VK']
                        if comb_present(comb, list_comb):
                            #print("ups, esta já existe:", end = '')
                            #print(comb)
                            #input()
                            continue
                        sum_w = float(0)
                        for cw in comb:
                            sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                        comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                        list_comb.append(comb_tup)
                        #print_comb(list_comb)
                        #print("k =",k)
                        #input()

                if k == 3:
                    for edge in edges:#edge = 'VK'
                        aux = [v.ide, edge]
                        for current_v in aux:#procurar os edges, para cada membro do aux!
                            new_edges = return_edges(problem, current_v)#new_edges = ['VCM','VDM']
                            for new_edge in new_edges:
                                if new_edge in aux:
                                    #print("ups, este está repetido:")
                                    #print("new_edge =", new_edge)
                                    #print("aux =", aux)
                                    #input()
                                    continue
                                comb = copy.copy(aux)#shallow copy
                                comb.append(new_edge)
                                #print("comb =", comb)
                                #print("new_edge =", new_edge)
                                #print("aux =", aux)
                                ##input()
                                if comb_present(comb, list_comb):
                                    #print("ups, esta já existe:", end = '')
                                    #print(comb)
                                    #input()
                                    continue
                                sum_w = float(0)
                                for cw in comb:
                                    sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                                comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                                list_comb.append(comb_tup)
                                #print_comb(list_comb)
                                #print("k =",k)
                                #input()
                    print_comb(list_comb)
                    print("fim do 3, k =",k)
                    input()

                if k == 4:
                    for edge in edges:#edge = 'VK'
                        if edge in aux:
                            #print("aux =", aux, "|", "edge =", edge)
                            #print("oi?!")
                            #input()
                            continue

                        aux2 = copy.copy(aux)#shallow copy
                        aux2.append(edge)

                        print("aux2 =", aux2)
                        input()

                        for current_v in aux2:#procurar os edges, para cada membro do aux!
                            new_edges = return_edges(problem, current_v)#new_edges = ['VCM','VDM']
                            for new_edge in new_edges:
                                #recursivo a partir daqui...

                                if new_edge in aux2:
                                    print("ups, este está repetido:")
                                    print("new_edge =", new_edge, "| aux2 =", end = "")
                                    print(aux2)
                                    input()
                                    continue
                                comb = copy.copy(aux2)#shallow copy
                                comb.append(new_edge)
                                print("comb =", comb)
                                print("new_edge =", new_edge)
                                print("aux2 =", aux2)
                                #input()
                                if comb_present(comb, list_comb):
                                    print("ups, esta já existe:", end = '')
                                    print(comb)
                                    input()
                                    continue
                                sum_w = float(0)
                                for cw in comb:
                                    sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                                comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                                list_comb.append(comb_tup)
                                print_comb(list_comb)
                                print("k =",k)
                                input()

                if k == 9:
                    #completa esta merda!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    comb = [v.ide]
                    if comb_present(comb, list_comb):
                    sum_w = float(0)
                    for cw in comb:
                        sum_w += list_V[cw]
                    comb_tup = (comb, sum_w)
                    list_comb.append(comb_tup)

                        
        #agora que geramos, vamos eliminar repetidas!
    print_comb(list_comb)
    print("chegamos ao fim!")
    input()
    input()
    input()
    input()
    input()
    input()
    input()
    input()
    input()
    input()

    return list_comb


def return_edges(problem, vertex_str):#vertex: vertex.ide = 'VDM'
    for ve in problem.v_list:#vamos ver agora todos os vizinhos do 'VDM'
        if ve.ide == vertex_str:
            edges = ve.c#edges tem agora uma lista de string com os vizinhos de VDM: ['VK']
            break#já encontramos; poupar ciclos
    return edges

def comb_present(comb, list_comb):
    is_present = False
    for comb_aux_tup in list_comb:
        comb_aux = comb_aux_tup[0]
        if sorted(comb) == sorted(comb_aux):
            is_present = True
            break
    #se não encontrou retorna False; se encontrou retorna True
    return is_present






##############################################################################################
##################       FIM DO NOVO generate_combinations()      ############################
##############################################################################################










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

def frontier_add_nodes(frontier, explored, list_comb, node_mother, problem, strategy):

    for c in list_comb: # c = ('manifest', sum_weight)
        node_aux = Node()
        state_aux = State()

        # populate state
        #state_aux.present = copy.deepcopy(node_mother.state.present)# aqui ele precisa MESMO do deepcopy...
        state_aux.present = copy.copy(node_mother.state.present)# aqui ele precisa MESMO do deepcopy...
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
                if verr.ide == vert_name:
                    if verr not in node_mother.state.manifest:
                        state_aux.manifest.append(verr)

        state_aux.depth_level = node_mother.state.depth_level + 1
        state_aux.launch = problem.l_list[state_aux.depth_level-1]

        #print("state_aux.depth_level = ", state_aux.depth_level)
        #print("node_mother.state.depth_level = ",node_mother.state.depth_level)


        # populate node
        node_aux.state = state_aux
        node_aux.g = node_mother.g + calculate_cost(state_aux.launch, state_aux.manifest, c[1])

        #node_aux.parent_node = copy.deepcopy(node_mother)
        node_aux.parent_node = node_mother

        # determine the h cost, based on strategy

        if strategy['search'].__name__ == 'Astar':
            node_aux.h = heur1(node_aux, problem)
            #node_aux.h = heur12(node_aux, problem)
            #node_aux.h = heur2(node_aux, problem)
            #node_aux.h = heur(node_aux, problem)
        else:
            node_aux.h = 0 #depois: node_aux.h = from_heuristic()
        #print("h =", str(node_aux.h))
        #input()


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
