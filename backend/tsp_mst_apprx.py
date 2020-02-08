import numpy as np
from edmonds import mst
from graph import Graph, Node

class Utils(object):
    def __init__(self, G):
        """
            G : class : <graph.Graph> 
        """
        self.G = G

    def computeMST(self, s):
        return self._constructGraph(mst(self.G, s))

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

    def _getPreOrderTraversal(self, root):
        if root:
            yield root.key
            self._getPreOrderTraversal(self._getNodeFromGraph(root.left))
            self._getPreOrderTraversal(self._getNodeFromGraph(root.right))

    def _getPostOrderTraversal(self, root):
        if root:
            self._getPostOrderTraversal(self._getNodeFromGraph(root.left))
            self._getPostOrderTraversal(self._getNodeFromGraph(root.right))
            yield root.key

    def _getInOrderTraversal(self, root):
        if root:
            self._getInOrderTraversal(self._getNodeFromGraph(root.left))
            yield root.key
            self._getInOrderTraversal(self._getNodeFromGraph(root.right))
            
    def PreOrderTraversal(self, G, node):
        return np.ndarray([n for n in self._getPreOrderTraversal(self._getNodeFromGraph( node))])

    def _getNodeFromGraph(self, node):
        return self.G.getBinaryTreeNode(node)
         
    
class TSPApproxMST(object):
    def __init__(self, G, s):
        self.G = G
        self.s = s
        self.utils_g = Utils(self.G)

    def getMSTPath(self):
        self.mst = self.utils_g.computeMST(self.s)
        self.preOrderTraversal = self.util_g.PreOrderTraversal(self.mst, self.s)
        return self.preOrderTraversal
        # Add path to graph utility function to return a graph here 

    def getTSPApproxMSTSoluction(self):
        path = self.getMSTPath()
        return self.G.getSolutionHamCycl(path)

