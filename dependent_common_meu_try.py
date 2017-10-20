# Python built-in libraries
import sys

class Vertex:

    def __init__(self):
        self.w = 0                  # Module weight
        self.c = []                 # List of modules which connect to this module
        self.ide = ''               # Module identification

class Launch:

    def __init__(self):
        self.d = []                   # Date of the launch
        self.mp = 0                   # Maximum payload of the launch
        self.fc = 0                   # Fixed cost of the launch
        self.vc = 0                   # Variable cost of the launch

class Node:

    def __init__(self):
        self.state = State()        # Node state
        self.g = 0                  # Path cost from the first node
        self.h = 0                  # Heuristic function
        self.parent_node = None     # Node that originated this one

#Nao percebo esta parte
class State:

    def __init__(self):
        self.pos = 'EXIT'           # Place id
        # Dictionary of stacks and CTS with correspondent casks ID. If a stack
        #or a CTS don't have a cask: delete
        self.cask_pos = {}

        # Auxiliary variables for heuristic calculation
        self.reached_goal_stack = False
        self.return2stack = False



class Problem:
    initial_state = None            # First Node state
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
            l.d = datetime.date(int(words[1][4:8]),int(words[1][2:4]),int(words[1][0:2]))
            l.mp = float(words[2])
            l.fc = float(words[3])
            l.vc = float(words[4])
            # adds it to the cask list
            l_list.append(v)

        elif line[0] == 'E':
            #adds connections to vertex class
            for v in v_list
                if v.ide == words[1]
                    v.c.append(words[1])
                elif v.ide == words[2]
                    v.c.append(words[1])

    l_list=sorted(l_list,key=lambda item: l.d)

    # initializes our problem
    problem = Problem()
    problem.initial_state=None
    problem.v_list = v_list
    problem.l_list = l_list
    problem.goal_state=len(v_list) # goal state is the number of vertex in space



    return problem
