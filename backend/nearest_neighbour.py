import numpy as np 

def get_nearest_neighbour(node):
    """
        This method returns the nearest neighbour of a node in a graph
        node : <class.Node> object
        returns : key of the nearest neighbour
    """
    min_w = np.argmin(node.weights)
    return node.children[min_w]

def get_second_nearest_neighbour(node):
    nearest = get_nearest_neighbour(node)
    rem_nearest_lst = np.delete(node.weights, node.key)
    out = np.argmin(rem_nearest_lst)
    return out
