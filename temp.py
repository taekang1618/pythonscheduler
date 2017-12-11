def isCyclicUtil(self, v, visited, recStack):

    # Mark current node as visited and
    # adds to recursion stack
    visited[v] = True
    recStack[v] = True

    # Recur for all neighbours
    # if any neighbour is visited and in
    # recStack then graph is cyclic
    for neighbour in self.graph[v]:
        if visited[neighbour] == False:
            if self.isCyclicUtil(neighbour, visited, recStack) == True:
                return True
        elif recStack[neighbour] == True:
            return True

    # The node needs to be poped from
    # recursion stack before function ends
    recStack[v] = False
    return False

# Returns true if graph is cyclic else false
def isCyclic(self):
    visited = [False] * self.V
    recStack = [False] * self.V
    for node in range(self.V):
        if visited[node] == False:
            if self.isCyclicUtil(node,visited,recStack) == True:
                return True
    return False
''' stack = []
DFS-B(G,s)
for all v in V[G] do
    visited[v] := false
end for
S := EmptyStack
visited[s] := true
Push(S,s)
while not Empty(S) do
    u := Pop(S)
    if there is at least one unvisited vertex in Adj[u] then
        Pick w to be any unvisited vertex in Adj[u]
        Push(S,u)
        visited[w] := true
        Push(S,w)
    end if
end while
'''
def toposort(graph):
    """Perform a topological sort on a graph
    This returns an ordering of the nodes in the graph that places all
    dependencies before the nodes that require them.
    Args:
        graph: an adjacency dict {node1: [dep1, dep2], node2: [dep1, dep3]}
    Returns:
        A list of ordered nodes
    """
    result = []
    used = set()

    def use(v, top):
        if v in used:
            return

        for parent in graph.get(v, []):
            if parent is top:
                raise ValueError("graph is cyclical through", parent)

            use(parent, v)

        used.add(v)
        result.append(v)

    for v in graph:
        use(v, v)

    return result
