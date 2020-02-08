import numpy as np 

def get_nearest_neighbour(node):
    """
        This method returns the nearest neighbour of a node in a graph
        node : <class.Node> object
        returns : key of the nearest neighbour
    """
    min_w = np.argmin(node.weights)
    return node.children[min_w]
