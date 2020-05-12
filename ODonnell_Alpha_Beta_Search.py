# Kyle O'Donnell
# CISC 481
# HW 2-Alpha-Beta Pruning


# Node class that stores various information regarding the nodes of the tree
class Node:
    def __init__(self, parent, t):
        self.parent = parent                        # stores the parent node
        self.child = []                             # stores the list of child nodes
        self.type = t
        self.alpha = -float('inf')
        self.beta = float('inf')
        if t == 'max':
            self.val = -float('inf')
        elif t == 'min':
            self.val = float('inf')


# initializes the program, takes user input, and generates the tree
def start():
    print('Type the starting configuration followed by the type of search.')
    print('Input:')
    leaf_nodes = input()
    leaf_nodes = leaf_nodes.split()
    for i in range(len(leaf_nodes)):
        leaf_nodes[i] = int(leaf_nodes[i])
    root_node = Node(None, 'max')
    index = 0
    for i in range(3):
        minimizer = Node(root_node, 'min')
        root_node.child += [minimizer]
        for j in range(2):
            maximizer = Node(minimizer, 'max')
            minimizer.child += [maximizer]
            for k in range(2):
                leaf = Node(maximizer, 'leaf')
                leaf.val = leaf_nodes[index]
                leaf.index = index
                index += 1
                maximizer.child += [leaf]
    return root_node


# begins the pruning process
def prune(root_node):
    to_prune = []
    prune_helper(root_node, to_prune)
    return to_prune


# recursively prunes the tree
def prune_helper(node, to_prune):
    for c in node.child:
        c.alpha = node.alpha
        c.beta = node.beta
        if node.type == 'max':
            if c.type == 'leaf':        # conditions if the node is ahead of the leafs
                if (c.val < node.beta) and (c.val > node.alpha):
                    node.alpha = c.val
                    node.val = node.alpha
                elif c.val >= node.alpha:       # updates maximizer with greatest value
                    node.alpha = c.val
                    node.val = node.alpha
                elif c.val > node.beta:
                    index_find(c, to_prune)
            else:
                if node.alpha <= c.beta:      # if the best option for the maximizer is less than the best option for
                    # the minimizer, move down that branch
                    prune_helper(c, to_prune)
                if c.val >= node.alpha:
                    node.alpha = c.val
                    node.val = node.alpha
                elif c.val <= node.alpha:      # prunes nodes if they are worse option for maximizer than already found
                    index_find(c, to_prune)
        elif node.type == 'min':
            if node.beta > c.alpha:     # if the best option for the minimizer is greater than the best option for
                # the maximizer, move down that branch
                prune_helper(c, to_prune)
            if c.val <= node.beta:        # updates minimizer with lowest value
                node.beta = c.val
                node.val = node.beta
            elif c.val >= node.beta:        # removes values that are worse for minimizer than found value
                index_find(c, to_prune)


# compiles list of indexes to prune
def index_find(node, to_prune):
    if node.type == 'leaf':
        to_prune += [node.index]
    else:
        for n in node.child:
            index_find(n, to_prune)


root = start()
pruned_nodes = prune(root)
print(pruned_nodes)
