import sys
import datetime
import copy
from itertools import combinations
from solver_library import *

################################################################################

class Vertex:

    def __init__(self):
        self.w = float(0)           # Module weight
        self.c = []                 # List of modules which connect to
                                    # this module (list of strings)
        self.ide = ''               # Module name(string)

class Launch:

    def __init__(self):
        self.date = []              # Date of the launch (date format)
        self.mp = 0                 # Maximum payload of the launch
        self.fc = 0                 # Fixed cost of the launch
        self.vc = 0                 # Variable cost of the launch

class Node:

    def __init__(self):
        self.state = State()        # Node state
        self.g = 0                  # Path cost from the first node
        self.h = 0                  # Heuristic function
        self.parent_node = None     # Node that originated this one

class State:

    def __init__(self):

        self.manifest = []           # list of vertices that are going in this launch
        self.present=[]
        self.depth_level = 0
        self.launch = Launch() # arranja maneira de meter cada node.state com um unico launch! acho que é mais fácil assim
        #self.launches = []           # list of past launch dates
        # Auxiliary variables for heuristic calculation
        #self.reached_goal_stack = False
        #self.return2stack = False

class Problem:
    l_list = None                   # List of scheduled launches
    v_list = set()                   # List of Modules to launch    #initial_state = 0              # First Node state - 0 vertex in space
    total_weight = 0                # Total weight of vertices to launch
    goal_state = 0                  # Number of vertices in space
    def v_list(self):
        return set(self.v_list)


###############################################################################
# order_file
#   Reorders the initial file: first the vertex lines, then the launch lines,
# and finaly, the Edge lines.
# Input: file_name
# Output: list of strings with each line type ordered

def order_file(file_name):

    with open(file_name) as f:
        v_file = []
        e_file = []
        l_file = []

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
#   Function that reads the input file and defines the problem, ordering the
# launches by date
# Input: file_name
# Output: problem

def read_file(file_name):
    v_list = []     # list of modules with the info of each module
    l_list = []     # list of launches (Launch)
    l_aux = Launch()
    #creates auxiliary launch
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

        elif line[0] == 'E':
            # adds connections to the respective Vertex classes
            for v in v_list:
                if v.ide == words[1]:
                    v.c.append(words[2])
                elif v.ide == words[2]:
                    v.c.append(words[1])

        elif line[0] == 'L':
            # initializes the Launch class
            l = Launch()
            l.date = datetime.date(int(words[1][4:8]), int(words[1][2:4]), int(words[1][0:2]))
            l.mp = float(words[2])
            l.fc = float(words[3])
            l.vc = float(words[4])
            l_list.append(l)

    # orders launch list by date
    l_list = sorted(l_list, key=lambda item: item.date)

    # initializes our Problem
    problem = Problem()
    problem.v_list = v_list
    problem.l_list = l_list
    sum_w = float(0)
    for vertex in v_list:
        sum_w += vertex.w
    problem.total_weight = sum_w
    problem.goal_state = len(v_list) # number of vertices in space

    print("vertex w c")
    for v in v_list:
        print(v.ide, v.w, v.c)
    print("\nlaunch: date mp fc vc")
    for l in l_list:
        print(l.date, l.mp, l.fc, l.vc)

    return problem

###############################################################################
# choose_node
#   Chooses node to be expanded next according to strategy
# Input: frontier, strategy
# Output: node to be expanded next

def choose_node(frontier, strategy):

    n_node = strategy['search'](frontier) # n_node: node position on frontier

    node = frontier[n_node]

    return node

###############################################################################
# goal_check
#   Checks if goal is achieved
# Input: state, problem
# Output: goal - 1 if achieved, 0 if not

def goal_check(state, problem):

    goal = 0
    if len(state.present)+len(state.manifest) == problem.goal_state:
        goal = 1 # Every component in orbit!
        print("@ goal")
        print_state(state)
    return goal

###############################################################################
# generate_answer
#   When the goal is found, the function writes the sequence of actions and cost
# Input: node
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

###############################################################################
# expand_node
#   Expands all the possible nodes that are reachable from the current node.
# Essential part of the program, taking into consideration all the constraints.
# Only expands a certain node if is not on the frontier  and, in the case it is
# on the frontier list, chooses the one with the lowest cost.
# Input: frontier, explored, node_mother, problem, strategy
# Output: frontier, explored
def expand_node(frontier, explored, node_mother, problem, strategy):

    if not node_mother.parent_node:
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
    #print("after launched filter - ",len(vertex_tl))
    #for vert2 in vertex_tl:
    #    print(" ", vert2.ide, end="")
    #print(" ")

    vertex_tl = filter_manifest(vertex_tl, node_mother)
    #print("after manifest filter - ",len(vertex_tl))
    #for vert2 in vertex_tl:
    #    print(" ", vert2.ide, end="")
    #print(" ")


    con_list = generate_combinations(vertex_tl)

    con_list = filter_weight(con_list, problem.l_list[node_mother.state.depth_level].mp)
    #print("after weight filter - ",len(con_list))

    graph=[]
    if len(vertex_tl)!=len(problem.v_list):
        graph=node_mother.state.manifest+node_mother.state.present
    #print(len(con_list))

    for con in con_list:
        for vert_string in con[0]:
            for vert in problem.v_list:
                if vert_string==vert.ide:
                    graph.append(vert)
                    # Put all the nodes together in one big set.
        nodes = set(graph)
                    # Find all the connected components.

        for components in connected_components(nodes, problem):
            if len(components)!=len(nodes):
                con_list.remove(con)
                continue

    #print(con_list)
    #print(" ")
    # add new created nodes to frontier
    frontier_add_nodes(frontier, explored, con_list, node_mother, problem, strategy)


    return frontier, explored

###############################################################################

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


###############################################################################



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

###############################################################################
# connected_components
#   Helps check if there are any unconected nodes in a graph
# Input: set of vertex, problem
# Output: List of groups of nodes (several if unconected vertex, one if conn.)
def connected_components(nodes, problem):

    # List of connected components found. The order is random.
    result = []

    # Make a copy of the set, so we can modify it.
    nodes = set(nodes)

    # Iterate while we still have nodes to process.
    while nodes:

        # Get a random node and remove it from the global set.
        n = nodes.pop()
        # This set will contain the next group of nodes connected to each other.
        group = {n}
        # Build a queue with this node in it.
        queue = [n]
        # Iterate the queue.
        # When it's empty, we finished visiting a group of connected nodes.
        while queue:
            # Consume the next item from the queue.
            n = queue.pop(0)
            # Fetch the neighbors.
            listaa=[]
            for vertex in problem.v_list:
                for conn in n.c:
                    if conn==vertex.ide:
                        listaa.append(vertex)

            neighbors =set(listaa)
            # Remove the neighbors we already visited.
            neighbors.difference_update(group)
            # Remove the remaining nodes from the global set.
            nodes.difference_update(neighbors)
            # Add them to the group of connected nodes.
            group.update(neighbors)
            # Add them to the queue, so we visit them in the next iterations.
            queue.extend(neighbors)
        # Add the group to the list of groups.
        result.append(group)
    # Return the list of groups.
    return result

###############################################################################
# frontier_add_nodes
#   Adds new nodes to frontier, using the launch combinations previously
# calculated and the parent nodes.
# Input: frontier, explored, list_comb, node_mother, problem, strategy
# Output: (simply modifies the frontier list)

def frontier_add_nodes(frontier, explored, list_comb, node_mother, problem, strategy):

    for c in list_comb: # c = ('manifest', sum_weight)
        node_aux = Node()
        state_aux = State()

        # populate state
        state_aux.present = copy.copy(node_mother.state.present)
        for pc in node_mother.state.manifest:
            if pc not in state_aux.present:
                state_aux.present.append(pc)

        for vert_name in c[0]:
            for  verr in problem.v_list:
                if verr.ide==vert_name:
                    if verr not in node_mother.state.manifest:
                        state_aux.manifest.append(verr)

        state_aux.depth_level = node_mother.state.depth_level + 1
        state_aux.launch = problem.l_list[state_aux.depth_level-1]

        # populate node
        node_aux.state = state_aux
        node_aux.g = node_mother.g + calculate_cost(state_aux.launch, state_aux.manifest, c[1])
        node_aux.parent_node = node_mother

        # determine the h cost, based on strategy
        if strategy['search'].__name__ == 'Astar':
            node_aux.h = heur1(node_aux, problem)
            #node_aux.h = heur12(node_aux, problem)
            #node_aux.h = heur2(node_aux, problem)
            #node_aux.h = heur(node_aux, problem)
        else:
            node_aux.h = 0 #depois: node_aux.h = from_heuristic()

        frontier.append(node_aux)
