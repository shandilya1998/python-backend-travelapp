import numpy as np
from graph import Node


"""
    Dijikistra's algorithm for calculating the shortest path between two nodes
    Input : node or int
"""
class DijkstraPath(object):
    def __init__(self, graph, s, t):
        self.graph = graph
        if isinstance(s, int):
            self.s = self.graph.getNode(s)
        else:
            self.s = s
        self.path = np.ndarray([self.s.index])
        self.t = t

    def compute_shortest_path(self):
        for node in self.graph.nodes:
            node = self.graph.getNode(node)
            nxt = node.children[np.argmin(node.nodeWeights)]  
            self.path = np.append(self.path, nxt)
            if nxt == self.t.index:
                break
        if self.path[-1] != self.t.index:
            return 'No path found'
        return self.path
            


    
