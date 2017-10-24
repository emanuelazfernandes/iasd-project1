# Python built-in libraries
import sys
import datetime

class Vertex:

    def __init__(self):
        self.w = 0                  # Module weight
        self.c = []                 # List of modules which connect to this module
        self.ide = ''               # Module identification

class Launch:

    def __init__(self):
        self.date = []                # Date of the launch
        self.mp = 0                   # Maximum payload of the launch
        self.fc = 0                   # Fixed cost of the launch
        self.vc = 0                   # Variable cost of the launch

class Node:

    def __init__(self):
        self.state = State()         # Node state
        self.g = 0                  # Path cost from the first node
        self.h = 0                  # Heuristic function
        self.parent_node = None     # Node that originated this one

class State:

    def __init__(self):
        self.present = []            # list of vertex in space
        self.launches = []           # list of past launch dates
        # Auxiliary variables for heuristic calculation
        #self.reached_goal_stack = False
        #self.return2stack = False


class Problem:
    #initial_state = 0               # First Node state - 0 vertex in space
    l_list = None                   # List of scheduled launches
    v_list = None                   # List of Modules to launch
    goal_state = 0                  # Number of vertex in space


################################################################################
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

################################################################################
# read_file
# Function that reads the input file and defines the problem
# Input: file_name
# Output: problem

def read_file(file_name):
    v_list = []     # list of module with the info of each modele (w, connections, etc ...)
    l_list = []     # list of launches
    #pid_list = []   # list of places id
    #cask_dict = {}  # dictionary of CTS and stacks and correspondent casks

    # gets ordered version of the input file
    ordered_file = order_file(file_name)

    for line in ordered_file:

        # removes '\n' character
        line = line.rstrip()
        # splits every word in the line seperated by whitespace
        words = line.split()

        if line[0] == 'V':
            # initializes the Vertex class
            v = Vertex()
            v.ide = words[0]
            v.w = float(words[1])
            # adds it to the cask list
            v_list.append(v)


        elif line[0] == 'L':
            # initializes the Launch class
            l = Launch()
            l.date = datetime.date(int(words[1][4:8]),int(words[1][2:4]),int(words[1][0:2]))
            l.mp = float(words[2])
            l.fc = float(words[3])
            l.vc = float(words[4])
            # adds it to the cask list
            l_list.append(l)

        elif line[0] == 'E':
            #adds connections to vertex class
            for v in v_list:
                if v.ide == words[1]:
                    v.c.append(words[2])
                elif v.ide == words[2]:
                    v.c.append(words[1])

    l_list=sorted(l_list,key=lambda item: item.date)

    # initializes our problem
    problem = Problem()
    problem.initial_state=0
    problem.v_list = v_list
    problem.l_list = l_list
    problem.goal_state=len(v_list) # goal state is the number of vertex in space

    print("vertex")
    for v in v_list:
        print(v.ide, v.w, v.c)
    print("launch")
    for l in l_list:
        print(l.date, l.mp, l.fc,l.vc)
    print("problem")
    print(problem.initial_state, problem.goal_state)


    return problem

###############################################################################
# choose_node
#   choose node to be expanded next according to strategy
# Input: frontier, strategy
# Output: node - to be expanded next

def choose_node (frontier, strategy):

    n_node = strategy['search'](frontier) # n_node: node position on frontier

    node = frontier[n_node]

    return node

###############################################################################
# goal_check
#   function that checks if goal is achieved
# Input: state, problem
# Output: goal - 1 if achieved, 0 if not

def goal_check (state, problem):

    if state == problem.goal:
        goal = 1 # CTS in on the exit point with the goal cask
    else:
        goal = 0

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

    ###gera ouutput, falta fazer

    return s, cost


###############################################################################
# expand_node
#   Expands all the possible nodes that are reachable from the current node.
# Essential part of the program, taking into consideration all the constraints.
# Only expands a certain node if is not on the frontier and explored list and,
# in the case it is on the frontier list, chooses the one with the lowest cost.
# Input: frontier, explored, node_mother, problem, strategy
# Output: frontier, explored

def expand_node (frontier, explored, node_mother, problem, strategy):

    vertex_tl = problem.v_list
    launch_av = problem.l_list
    search = strategy['search']         # search algorithm to be implemented


    #consider only launches that have not happened, and if a launch has happened ignore launces previous to that one
    for launch in problem.l_list:
        if launch in node_mother.state.launches:
            launch_av.remove(launch)
        if launch < max(node_mother.state.launches.date):
            launch_av.remove(launch)
    #we now have a list of the launches we have available

    #consider only unlaunched vertex
    for vertex in problem.v_list:
        if vertex in node_mother.state.present  #if vertex in space, it cant be launched
            vertex_tl.remove(vertex)

        #list of the eligible vertex to launch
        if vertex.c not in con_list
            con_list=con_list.append(vertex.c)


    #list with possible, launchable vertex
    for vertex in v_list
        if vertex.ide not in con_list
            v_list.remove(vertex)





    # generation of all the possible launch components combinations
def generate_combinations(list_V):
  list_comb = []

  #print("possible combinations: ")#debug
  for k in range(0,list_V.__len__()+1):#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
    #print(k,end = ': ')#debug
    comb_aux = list(combinations(list_V.keys(),k))#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
    for j in range(0,comb_aux.__len__()):#para meter todos na mesma lista...
      sum_weights = 0
      for w in comb_aux[j]:
        sum_weights = sum_weights + list_V[w]#sum the weights of the combination, DEIXA FICAR O V, POIS É O DICT ORIGINAL
      list_comb.append((comb_aux[j],sum_weights))
    #print(comb_aux)#debug
    #print(comb_aux.__len__())#debug
    #print()#debug
  #print()#debug

  #print_comb(list_comb)
  return list_comb
