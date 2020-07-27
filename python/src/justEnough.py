import random



class DoublePrimeRing():
	"""docstring for DoublePrimeRing"""
	def __init__(self, n, interval, bandwidth):
		super(DoublePrimeRing, self).__init__()
		self.n = n
		self.interval = interval
		self.linkBandwidth = bandwidth
	
	def constructGraph(self):
		edges = []
		#edges between vertices in core ring
		torNeighbour = 0
		for i in range(self.n):
			neighbours = []
			neighbours.append([self.n+torNeighbour%self.n, self.linkBandwidth])
			neighbours.append([(i+1)%self.n, self.linkBandwidth])
			neighbours.append([(i-1)%self.n, self.linkBandwidth])
			edges.append(neighbours)
			torNeighbour += 2
		#edges between vertices in tor ring
		coreNeighbour = 0
		for i in range(self.n):
			neighbours = []
			neighbours.append([coreNeighbour%self.n, self.linkBandwidth])
			neighbours.append([self.n + (i+1)%self.n, self.linkBandwidth])
			neighbours.append([self.n + (i-1)%self.n, self.linkBandwidth])
			neighbours.append([self.n + (i+self.interval)%self.n, self.linkBandwidth])
			neighbours.append([self.n + (i-self.interval)%self.n, self.linkBandwidth])
			edges.append(neighbours)
			torNeighbour += 4
		return edges

class LogicalGraph():
	"""docstring for LogicalGraph"""
	def __init__(self, type, size, bandwidth):
		super(LogicalGraph, self).__init__()
		self.size = size
		self.type = type
		self.linkBandwidth = bandwidth

	def constructGraph(self):
		if self.type == "linear":
			return self.constructLinearTopology()
		elif self.type == "star":
			return self.constructStarTopology()
		elif self.type == "tree":
			return self.constructTreeTopology()

	def constructLinearTopology(self):
		edges = []
		edges.append([[1, self.linkBandwidth],])
		for i in range(1,self.size-1):
			neighbours = []
			neighbours.append([(i+1)%self.size, self.linkBandwidth])
			neighbours.append([(i-1)%self.size, self.linkBandwidth])
			edges.append(neighbours)
		edges.append([[self.size-2, self.linkBandwidth],])
		return edges

	def constructStarTopology(self):
		edges = []
		edges.append([])
		for i in range(1,self.size):
			edges.append([[0, self.linkBandwidth],])
			edges[0].append([i, self.linkBandwidth])
		return edges
	
	def constructTreeTopology(self):
		edges = []
		#TODO - create tree
		return edges

def getNextNode(currentNode):
	return currentNode+1

def UpdatePath(parent, currentNode, root, G, required):
	previousNode = currentNode
	currentNode = parent[currentNode]
	while currentNode != root :
		for i in range(len(G[currentNode])):
			if G[currentNode][i][0] == previousNode:
				G[currentNode][i][1] -= required
				if G[i][1] < 0:
					return False

		previousNode = currentNode
		currentNode = parent[currentNode]
	return True
	

def getNearestNode(P, G, requiredEdgeCapacity, physicalVertexCapacity, requiredVertexCapacity):
	nodesToCheck = G[P]
	print(P, nodesToCheck)
	parent = [-1 for i in range(len(G))]
	while nodesToCheck:	#pick node with max physical constraint value
		iList = nodesToCheck.pop(0)
		i = iList[0]
		print(i)
		if i<int(len(G)/2) and physicalVertexCapacity[i] > requiredVertexCapacity:
			#you might want to experiment with choosing an unassigned node as well
			if UpdatePath(parent, i, P, G, requiredEdgeCapacity):
				return i
		nodesToCheck.extend(G[i])
		for j in G[i]:
			parent[j[0]] = i
	return -1


def mapSubgraph(G, H, sizePhysical, sizeLogical, physicalVertexCapacity, logicalVertexCapacity, type):
	L = 0 #node from logical topology


	P = random.randint(0,sizePhysical-1) 
	while physicalVertexCapacity[P] < logicalVertexCapacity[L]:
		P = random.randint(0,sizePhysical-1) 


	nodesToMap = sizeLogical
	mapping = [-1 for i in range(sizeLogical)]

	mapping[L] = P
	physicalVertexCapacity[P] -=logicalVertexCapacity[L ]
	nodesToMap -= 1

	while nodesToMap > 0:
		L = getNextNode(L)
		for (i,j) in H[L-1]:
			if i == L:
				requiredEdgeCapacity = j
		P = getNearestNode(P, G, requiredEdgeCapacity, physicalVertexCapacity, logicalVertexCapacity[L])
		if P == -1:
			return []
		mapping[L] = P[0]
		physicalVertexCapacity[P] -=logicalVertexCapacity[L]
		nodesToMap -= 1

	return mapping


def main():
	sizePhysical = 7
	sizeLogical = 25
	G = DoublePrimeRing(n=sizePhysical, interval=3, bandwidth = 15).constructGraph()
	physicalVertexCapacity = [10 for i in range(sizePhysical)]
	H = LogicalGraph(type = "linear", size=sizeLogical, bandwidth = 2).constructGraph()
	logicalVertexCapacity = [1 for i in range(sizeLogical)]
	
	print("PRINTING PHYSICAL GRAPH")
	for i in G:
		print(i)
	print("PRINTING LOGICAL GRAPH")
	for i in H:
		print(i)

	import time
	startTime = time.time()
	mapping = mapSubgraph(G, H, sizePhysical, sizeLogical, physicalVertexCapacity, logicalVertexCapacity, type="linear")
	# mapping = mapSubgraph(G, H, sizePhysical, sizeLogical, physicalVertexCapacity, logicalVertexCapacity, type="star")
	endTime = time.time()
	print("%s " %(endTime-startTime))

	if mapping:
		print("mapping found")
		print(mapping) 
	else:
		print("mapping not found :/")

	print("")

if __name__ == "__main__":
	main()
