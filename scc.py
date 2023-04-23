class Graph:
    def __init__(self, Vertices) -> None:
        self.V = Vertices
        self.curSCC = 0

class Vertex:
    def __init__(self, value) -> None:
        self.value = value
        self.explored = False
        self.numSCC = 0
        self.outgoing = []
        self.incoming = []

class Order:
    def __init__(self, n) -> None:
        self.arr = [None for _ in range(n)]
        self.rank = n-1
    
def printVertices(V):
    print('Vertex values:')
    for v in V:
        print(v.value)

def createGraph(filename):
    V, vSet = [], set()
    with open(filename, 'r') as file:
        n = 0
        for line in file:
            v1, v2 = line.split()            
            if v1 not in vSet:
                vSet.add(v1)
                n += 1
            if v2 not in vSet:
                vSet.add(v2)
                n += 1
        V = [Vertex(x+1) for x in range(n)]
        file.seek(0)
        for line in file:
            i1, i2 = [int(x) for x in line.split()]
            v1 = V[i1-1]
            v2 = V[i2-1]
            v1.outgoing.append(v2)
            v2.incoming.append(v1)
    return Graph(V) 

"""
Topological sort orders the 'farthest' node from the start 
the highest and the start node lower. The lowest ranked node
will always be in a source SCC, but we reverse the graph so
we can identify a sink SCC.

reverseTopoSort returns a list containing an ordering of all
the vertices in V. 
"""
def reverseTopoSort(G):
    magicOrder = Order(len(G.V))
    for v in G.V:
        if v.explored:
            continue
        topoDFS(v, magicOrder)
    return magicOrder.arr

def topoDFS(startNode, magicOrder):
    startNode.explored = True
    for v in startNode.incoming:
        if v.explored:
            continue
        topoDFS(v, magicOrder)
    magicOrder.arr[magicOrder.rank] = startNode
    magicOrder.rank -= 1
    return

def kosaraju(G):
    magicOrder = reverseTopoSort(G)
    for v in G.V:
        v.explored = False
    for v in magicOrder:
        if v.explored:
            continue
        G.curSCC += 1
        DFS_SCC(G, v)
    return

def DFS_SCC(G, startNode):
    if startNode.explored:
        return
    startNode.explored = True
    startNode.numSCC = G.curSCC
    for v in startNode.outgoing:
        DFS_SCC(G, v)
    return

def printSCCs(G):
    SCCs = {}
    for v in G.V:
        if v.numSCC in SCCs:
            SCCs[v.numSCC].append(v)
        else:
            SCCs[v.numSCC] = [v]
    for SCCnum in SCCs:
        print('SCC', SCCnum)
        printVertices(SCCs[SCCnum])
    return

def fiveLargestSCCSizes(G):
    SCCs = {}
    for v in G.V:
        if v.numSCC in SCCs:
            SCCs[v.numSCC] += 1
        else:
            SCCs[v.numSCC] = 1
    bigFive = [0,0,0,0,0]
    for n in SCCs:
        smallest = min(bigFive)
        if SCCs[n] > smallest:
            bigFive.remove(smallest)
            bigFive.append(SCCs[n])
    return sorted(bigFive, reverse=True)



filename = 'test1.txt'
G = createGraph(filename)
kosaraju(G)
answer = fiveLargestSCCSizes(G)
print(answer)

# printSCCs(G)
# G.printVertices()
# G.printEdges()
# printVertices(reverseTopoSort(G))