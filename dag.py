''' A Python Class for a directed acyclic graph of tasks.
Uses a dictionary to represent an adjacency list of the graph.
  ex) { 'A' : ['B', 'C'],
        'B' : ['C', 'E'],            A --> B --> E
        'C' : ['D'],           ==     \   /      |
        'D' : []                       V V       V
        'E' : ['D'] }                   C  ----> D

Uses depth first search to check for cycles when initializing and adding edges.
'''

import task
from collections import defaultdict

class DirectedAcyclicGraph(object):

    def __init__(self, vertices, edges=[]):
        ''' Initializes a graph in dictionary format with a list of vertices
        and edges.
        '''
        self.__vertexSet = vertices
        self.__edgeSet = edges
        self.__graph_dict = defaultdict(list)
        for v in vertices:
            self.__graph_dict[v] = []
        if edges:
            for k, v in edges:
                self.__graph_dict[k].append(v)


    def __str__(self):
        ''' Outputs stringified version of graph dictionary '''
        s = "{"
        if not self.__vertexSet:
            s += "}"
        else:
            for k, neighbors in self.__graph_dict.items():
                s += str(k) + ": ["
                if not neighbors:
                    s += "], \n "
                else:
                    for n in neighbors:
                        s += str(n) + ","
                    s = s[:-1] + "], \n "
            s = s[:-4] + "}"
        return s


    def graph(self):
        ''' returns the graph in dictionary format '''
        return self.__graph_dict

    def vertices(self):
        ''' returns the vertices of a graph '''
        return self.__vertexSet


    def edges(self):
        ''' returns the edges of a graph '''
        return self.__edgeSet


    def addVertex(self, vertex):
        ''' If vertex is not in graph_dict, a vertex key with an empty list as
        value is added to the dictionary. Otherwise do nothing.
        '''
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
            self.__vertexSet.append(vertex)

    def addEdge(self, edge):
        ''' Adds an edge (of tuple type) after checking if it creates cycles
        '''
        if edge in self.__edgeSet:
            print("Edge already exists in the graph!")
        else:
            (k, v) = tuple(edge)
            if k == v:
                print("Graph must be acyclic(self-edge)!")
            else:
                self.__graph_dict[k].append(v)
                if self.__isCyclic(k):
                    self.__graph_dict[k].remove(v)
                    print("Graph must be acyclic!")
                else:
                    self.addVertex(k)
                    self.addVertex(v)
                    self.__edgeSet.append(edge)


    def __cycleHelper(self, v, visited, stack):
        ''' Helper function to run __isCyclic'''
        visited[v] = True
        stack[v] = True
        for n in self.__graph_dict[v]:
            if visited[n] == False:
                if self.__cycleHelper(n, visited, stack):
                    return True
            elif stack[n] == True:
                return True
        stack[v] = False
        return False


    def __isCyclic(self, init_node):
        ''' Checks for cycles using the dfs algorithm. '''
        visited = defaultdict(bool)
        stack = defaultdict(bool)
        for v in self.__vertexSet:
            visited[v] = False
            stack[v] = False
        for v in self.__vertexSet:
            if self.__cycleHelper(v, visited, stack) == True:
                return True
        return False


    def __toposort_helper(self, v, top, used, result):
        if v in used:
            return
        for parent in self.__graph_dict[v]:
            self.__toposort_helper(parent, v, used, result)
        used.add(v)
        result.append(v)


    def toposort(self):
        ''' Helper function to topologically sort the directed acyclic graph '''
        result = []
        used = set()
        for v in self.__graph_dict:
            self.__toposort_helper(v, v, used, result)
        return result[::-1]


    def invertGraph(self):
        ''' Invert edges of the graph to get a dictionary of parent nodes. '''
        new_edges = []
        for e in self.__edgeSet:
            (v1, v2) = e
            new_edges.append((v2, v1))
        return DirectedAcyclicGraph(self.__vertexSet, new_edges)
