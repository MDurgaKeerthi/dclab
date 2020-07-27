import random



class DoublePrimeRing():
	"""docstring for DoublePrimeRing"""
	def __init__(self, n, interval):
		#super(DoublePrimeRing, self).__init__()
		self.n = n
		self.interval = interval
		# self.constructGraph()
	
	def constructGraph(self):
		edges = []
		#edges between vertices in core ring
		torNeighbour = 0
		for i in range(self.n):
			neighbours = []
			neighbours.append(self.n+torNeighbour%self.n)
			neighbours.append((i+1)%self.n)
			neighbours.append((i-1)%self.n)
			edges.append(neighbours)
			torNeighbour += 2
		#edges between vertices in tor ring
		coreNeighbour = 0
		for i in range(self.n):
			neighbours = []
			neighbours.append(coreNeighbour%self.n)
			neighbours.append(self.n + (i+1)%self.n)
			neighbours.append(self.n + (i-1)%self.n)
			neighbours.append(self.n + (i+self.interval)%self.n)
			neighbours.append(self.n + (i-self.interval)%self.n)
			edges.append(neighbours)
			torNeighbour += 4
		return edges

class LogicalGraph():
	"""docstring for LogicalGraph"""
	def __init__(self, type, size):
		super(LogicalGraph, self).__init__()
		self.size = size
		# self.edges = []
		self.type = type

	def constructGraph(self):
		if self.type == "linear":
			return self.constructLinearTopology()
		elif self.type == "star":
			return self.constructStarTopology()
		elif self.type == "tree":
			return self.constructTreeTopology()

	def constructLinearTopology(self):
		edges = []
		edges.append([1])
		for i in range(1,self.size-1):
			neighbours = []
			neighbours.append((i+1)%self.size)
			neighbours.append((i-1)%self.size)
			edges.append(neighbours)
		edges.append([self.size-2])
		return edges

	def constructStarTopology(self):
		edges = []
		edges.append([])
		for i in range(1,self.size):
			edges.append([0])
			edges[0].append(i)
		return edges
	
	def constructTreeTopology(self):
		edges = []
		#TODO - create tree
		return edges

def getNextNode(currentNode):
	return currentNode+1
	# if type == "linear":
	# 	return currentNode+1
	# elif type == "star":
	# 	if currentNode == 0:
	# 		return currentNode

def getNearestNode(P,G, unmapped):
	nodesToCheck = G[P]
	visited = [False for i in range(int(len(G)/2))]
	print(P, nodesToCheck)
	while nodesToCheck:	#pick node with max physical constraint value
		i = nodesToCheck.pop(0)
		print(i)
		if i in unmapped:
			return i
		nodesToCheck.extend(G[i])
	return -1


def mapSubgraph(G, H, sizePhysical, sizeLogical, physicalConstraints, logicalConstraints, type):
	L = 0 #node from logical topology
	P = random.randint(0,sizePhysical-1) #pick node with max physical constraint value
	nodesToMap = sizeLogical
	mapping = [-1 for i in range(sizeLogical)]
	unmapped = [i for i in range(sizePhysical)]
	while nodesToMap > 0:
		mapping[L] = P
		unmapped.remove(P)
		nodesToMap -= 1
		P = getNearestNode(P, G, unmapped)
		if P == -1:
			return []
		L = getNextNode(L)
	return mapping


def main():
	sizePhysical = 7
	sizeLogical = 4
	G = DoublePrimeRing(n=sizePhysical, interval=3).constructGraph()
	physicalConstraints = [10 for i in range(sizePhysical)]
	H = LogicalGraph(type = "linear", size=sizeLogical).constructGraph()
	logicalConstraints = [1 for i in range(sizeLogical)]
	
	for i in G:
		print(i)
	for i in H:
		print(i)

	mapping = mapSubgraph(G, H, sizePhysical, sizeLogical, physicalConstraints, logicalConstraints, type="linear")
	if mapping:
		print("mapping found")
		print(mapping) 
	else:
		print("mapping not found :/")


if __name__ == "__main__":
	main()
