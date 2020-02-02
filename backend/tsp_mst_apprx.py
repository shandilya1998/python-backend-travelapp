import numpy as np
from edmonds import mst
from graph import Graph

class Utils(object):
    def __init__(self, G):
        """
            G : class : <graph.Graph> 
        """
        self.G = G

    def _computeMST(self):
        return self._constructGraph(mst(self.G))

    def _constructGraph(self, g):
        """
            g : dict with nodes are keys and list of neighbours as elements
        """
        nodes = g.keys()
        row = self._compute_row(g)
        col = self._conpute_col(g)
        G = Graph(row, col, nodes)
        for node in nodes:
            for ele in g[node]:
                G.connect_dir(node, ele)
        return G

    def _getPreOrderTraversal(root):
            if root:
                 _getPreOrderTraversal


