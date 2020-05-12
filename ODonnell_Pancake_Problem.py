# Kyle O'Donnell
# CISC 481
# HW 1-U-Pancake

# Class that groups all necessary data of each node together for ease of use
class PancakeStack:
    def __init__(self, pan_stack, parent):
        self.stack = pan_stack                      # pan_stack data is implemented as a list of characters
        self.parent = parent                        # stores the parent node
        self.nodes = []                             # stores the list of child nodes
        self.p_flip = -1                            # stores where the parent had to flip to achieve this configuration
        self.h = 0
        self.g = 0
        self.f = 0
        self.path = [self]                          # stores path to current node from root


# Method that takes user input and properly formats data for searches
def start():
    print('Type the starting configuration followed by the type of search.')
    print('Input:')
    start_stack = input()
    formatted_stack = list(start_stack)[:4]
    search_type = start_stack[4:]
    return formatted_stack, search_type


# Implementation of Depth First Search
# Fringe is implemented through recursively visiting added newest added nodes
def depth_first_search(node, visited):
    visited += [node.stack]     # begins by adding the current node's configuration to the closed set
    if node.stack == ['4', '3', '2', '1']:      # base case, returns path
        return node.path
    for i in range(1, 4):       # creates and properly initializes all unexpanded child nodes
        child_stack = node.stack[0:3 - i:1] + node.stack[3:-i - 2:-1]
        if child_stack not in visited:
            visited += [child_stack]
            child = PancakeStack(child_stack, node)
            child.p_flip = 3 - i
            child.g = node.g + i + 1
            child.path = node.path + [child]
            node.nodes += [child]
    for i in range(len(node.nodes)):        # iterates through all possible child nodes
        path = depth_first_search(node.nodes[i], visited)
        if path:
            return path
        else:
            return False


# Implementation of A* Search
# Fringe is implemented with a priority queue in the form of a list.  Newly created children are sorted into the list
# which is traversed in order.
def a_star_search(node, visited, queue):
    visited += [node.stack]
    if node.stack == ['4', '3', '2', '1']:
        return node.path
    for i in range(1, 4):
        child_stack = node.stack[0:3 - i:1] + node.stack[3:-i-2:-1]
        if child_stack not in visited:
            visited += [child_stack]
            child = PancakeStack(child_stack, node)
            child.p_flip = 3-i
            child.g = node.g + i + 1
            h(child)
            child.path = node.path + [child]
            child.f = child.g + child.h
            node.nodes += [child]
            queue = insert_in_queue(child, queue)
    for i in range(len(queue)):
        path = a_star_search(queue[0], visited, queue[1:])
        if path:
            return path
        else:
            return False


# Method utilized to print output of Depth First Search
def print_dfs(soln):
    for i in range(len(soln)):
        if soln[i].nodes:
            string = soln[i].stack[0:int(soln[i+1].p_flip):1]+['|']+soln[i].stack[int(soln[i+1].p_flip):]
        else:
            string = soln[i].stack
        str_stack = ''
        for c in string:
            str_stack += c
        print(str_stack + '; g = ' + str(soln[i].g))


# Method utilized to print output of A* Search
def print_a_star(soln):
    for i in range(len(soln)):
        if soln[i].nodes:
            string = soln[i].stack[0:int(soln[i+1].p_flip):1]+['|']+soln[i].stack[int(soln[i+1].p_flip):]
        else:
            string = soln[i].stack
        str_stack = ''
        for c in string:
            str_stack += c
        print(str_stack + '; g = ' + str(soln[i].g) + '; h = ' + str(soln[i].h))


# Method that calculates and sets the heuristic used by A* search
def h(node):
    if node.stack[0] != '4':
        node.h = 4
    elif node.stack[1] != '3':
        node.h = 3
    elif node.stack[2] != '2':
        node.h = 2
    elif node.stack[3] != '1':
        node.h = 1
    else:
        node.h = 0


# Method that inserts new children within the priority queue
def insert_in_queue(node, queue):
    new_queue = []
    if not queue:       # adds first node to empty list
        new_queue += [node]
        return new_queue
    elif node.f < queue[0].f:       # if new node has lower f value than first list element, add to front
        new_queue = [node] + queue
        return new_queue
    elif node.f <= queue[-1].f:     # if new node's f value lies within bounds of list, insert in place
        for i in range(len(queue)):
            if node.f < queue[i].f:
                new_queue = queue[0:i] + [node] + queue[i:]
                return new_queue
            elif node.f == queue[i].f:      # handles ties in value of f
                if numerical(node.stack) > numerical(queue[i].stack):
                    new_queue = queue[0:i] + [node] + queue[i:]
                    return new_queue
                else:
                    new_queue = queue[0:i] + [node] + queue[i:]
                    return new_queue
    else:       # adds new node at end
        new_queue = queue + [node]
        return new_queue


# Helper function for tie-breakers when inserting in priority queue
def numerical(order):
    return int(order[0])*1000 + int(order[1])*100 + int(order[2])*10 + int(order[3])


stack, search = start()     # asks for, and formats user input

root = PancakeStack(stack, None)        # initializes root node
h(root)
closed_set = []     # initializes closed set of expanded values
priority_queue = []     # initializes priority queue as list

if search == 'd':       # Depth First Search selected
    print('Depth-First Search selected')
    print('Output:')
    dfs_path = depth_first_search(root, closed_set)
    print_dfs(dfs_path)
elif search == 'a':     # A* Search selected
    print('A* Search selected')
    a_star_path = a_star_search(root, closed_set, priority_queue)
    print_a_star(a_star_path)
