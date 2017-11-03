

# The function to look for connected components.
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


# Python built-in libraries
import sys
import time

# User scripts
from domain_independent import general_search
from domain_dependent import *
from solver_library import *


# The test code...
if __name__ == "__main__":

    problem = read_file("meu.txt")


    # Put all the nodes together in one big set.
    nodes = set(problem.v_list)

    # Find all the connected components.
    number = 1
    for components in connected_components(nodes, problem):
        if len(components)!=len(nodes):
            print("not CONN")
        names = sorted(node.ide for node in components)
        print(len(connected_components(nodes, problem)))
        names = ", ".join(names)
        print ("Group #%i: %s" % (number, names))
        number += 1
