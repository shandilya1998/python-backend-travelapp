import numpy as np

class Node:
    """
        This is the base class for a generic node of a graph
        This is compatible with any graph data structure
    """

    def __init__(self, index, children = None, edgeWeights = None, nodeWeight = None):
        self.index = index
        self.children = children
        self.edgeWeights = edgeWeights
        self.nodeWeight = nodeWeight

class BinaryTreeNode:

    """
        This is the base class for a inheriting properties of a node.
        This is compatible with any graph data structure
    """
  
    def __init__(self, key, indexloc = None, left = None, right = None):
        self.key = key
        self.index = indexloc
        self.left = left
        self.right = right
        
       
class Graph(dict):

    @classmethod
    def create_from_nodes(self, nodes):
        return Graph(len(nodes), len(nodes), nodes)

  
    def __init__(self, 
                 row,
                 col = None,
                 nodes = None,
                 weights = None,
                 connection = 'from', 
                 complete = False, 
                 binary = False):
        """
            The class sets-up aan adjacency matrix 
            row : number of nodes in the graph from wich connections originate; Required; int
            col : number of nodes in the graph to which connections go; Optional; int, default : row
            nodes : array containing the indices of all the nodes; Optional; np.array or np.ndarray; 
                    default : np.ndarray([0, 1, 2, 3, 4,..., row])
            weights : array containing the weights corresponding to each node; np.ndarray; Optional;
                      default : mp.ndarray([1])
            connection : set type of connection - 'to' or 'from'; Optional, defualt : 'from'
            complete : Boolean, if the graph is complete or not
            binary : Boolean, if the graph is binary or not

        """
        if not col:
            col = row
        self.connection = connection
        self.complete = complete
        self.binary = binary
        if not complete:
            self.adj_mat = np.zeros((row, col))
        else:
            self.adj_mat = np.ones((row, col))
        if not nodes:
            nodes = np.arange(row)
        self.nodes = nodes
        if not weights:
            weights = np.ones(row)
        self.weights = weights
        super(Graph, self).__init__()

    def getBinaryTreeNode(self, index):
        if self.binary:
            node = BinaryTreeNode(key = index)
            if self.connection == 'from':
                connections = self.connections_from(index)
            elif self.connection == 'to':
                connections = self.connections_to(index)
            if connections[0]<connections[1]:
                left = connections[0]
                right = connections[1]
            else:
                left = connections[1]
                right = connections[0]
            node.left = left
            node.right = right
            return node
        else:
            raise TypeError('The graph is not a binary tree')

    def getNode(self, index):
        if self.connection == 'from':
            children = self.connections_from(index)
        elif self.connection == 'to':
            children = self.connection_to(index)
        node = Node(index, children = children)
        return node

    """
        Connects from node1 to node2
        Note row is source, column is destination
        Updated to allow weighted edges (supporting dijkstra's alg)
    """
    def connect_dir(self, node1, node2, weight = 1):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = weight
  
    # Optional weight argument to support dijkstra's alg
    def connect(self, node1, node2, weight = 1):
        self.connect_dir(node1, node2, weight)
        self.connect_dir(node2, node1, weight)

    
    """
        Get node row, map non-zero items to their node in the self.nodes array
        Select any non-zero elements, leaving you with an array of nodes
        which are connections_to (for a directed graph)
        Return value: array of tuples (node, weight)
    """
    def connections_from(self, node):
        """
            returns all connections from a node with their respective weights
            List of tuples
        """
        node = self.get_index_from_node(node)
        return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if self.adj_mat[node][col_num] != 0]

    """
        Map matrix to column of node
        Map any non-zero elements to the node at that row index
        Select only non-zero elements
        Note for a non-directed graph, you can use connections_to OR
        connections_from
        Return value: array of tuples (node, weight)
    """

    def connections_to(self, node):
        node = self.get_index_from_node(node)
        column = [row[node] for row in self.adj_mat]
        return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]
     
  
    def print_adj_mat(self):
        for row in self.adj_mat:
             print(row)
   
  
    def remove_conn(self, node1, node2):
        self.remove_conn_dir(node1, node2)
        self.remove_conn_dir(node2, node1)
   
    """
        Remove connection in a directed manner (nod1 to node2)
        Can accept index number OR node object
    """
    def remove_conn_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        self.adj_mat[node1][node2] = 0   
  
    """
        Can go from node 1 to node 2?
    """
    def can_traverse_dir(self, node1, node2):
        node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
        return self.adj_mat[node1][node2] != 0  
  
    def has_conn(self, node1, node2):
        return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)
  
    def add_node(self, node):
        self.nodes = np.append(self.nodes, [node])
        node.index = len(self.nodes) - 1
        self.adj_mat = np.append(self.a)     
        self.adj_mat.append([0] * (len(self.adj_mat) + 1))

    """
        Get the weight associated with travelling from n1
        to n2. Can accept index numbers OR node objects
    """
    def get_weight(self, n1, n2):
        node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
        return self.adj_mat[node1][node2]
  
    """
        Allows either node OR node indices to be passed into 
    """
    def get_index_from_node(self, node):
        if not isinstance(node, Node) and not isinstance(node, int):
            raise ValueError("node must be an integer or a Node object")
        if isinstance(node, int):
            return node
        else:
            return node.index

    """ 
        Check if this vertex is an adjacent vertex
        of the previously added vertex and is not
        included in the path earlier 
    """
    def isSafe(self, node, index, path):
        # Check if current vertex and last vertex
        # in path are adjacent
        if self.adj_mat[path[index-1]][node] == 0:
            return False

        # Check if current vertex not already in path
        for vertex in path:
            if vertex == node:
                return False

        return True

    """
        A recursive utility function to solve
        hamiltonian cycle problem
    """
    def hamCycleUtil(self, path, index):

        # base case: if all vertices are
        # included in the path
        if index == self.nodes.shape[0]:
            # Last vertex must be adjacent to the
            # first vertex in path to make a cyle
            if self.adj_mat[ path[index-1] ][ path[0] ] == 1:
                return True
            else:
                return False

        # Try different vertices as a next candidate
        # in Hamiltonian Cycle. We don't try for 0 as
        # we included 0 as starting point in hamCycle()
        for v in range(1, self.nodes.shape[0]):

            if self.isSafe(v, index, path) == True:

                path[index] = v

                if self.hamCycleUtil(path, index+1) == True:
                    return True

                # Remove current vertex if it doesn't
                # lead to a solution
                path[index] = -1

        return False

    def hamCycle(self):
        path = [-1] * self.nodes.shape[0]

        """ 
            Let us put vertex 0 as the first vertex
            in the path. If there is a Hamiltonian Cycle,
            then the path can be started from any point
            of the cycle as the graph is undirected
        """
        path[0] = 0

        if self.hamCycleUtil(path,1) == False:
            print ("Solution does not exist\n")
            return False

        self.printSolutionHamCycl(path)
        return True

    def printSolutionHamCycl(self, path):
        print ("Solution Exists: Following",
                 "is one Hamiltonian Cycle")
        for vertex in path:
            print (vertex, end = " ")
        print (path[0], "\n")

    def getSolutionHamCycl(self, path):
        for vertex in path:
            yield vertex
    
    def __getattr__(self, vertex):
        if self.connection == 'to':
            return self.connections_to(vertex)
        elif self.connection == 'from':
            return self.connections_from(vertex)

g = Graph(10)  

