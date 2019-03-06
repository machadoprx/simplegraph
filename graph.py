from heap import Heap
from fibonacci import FibonacciHeap
import time

class Vertex:

	def __init__(self, data):
		self.data = data
		self.color = 0
		self.dist = float('inf')
		self.prev = None
		self.adj = {}

	def addNeighbor(self, neighbor, weight = 0):
		self.adj[neighbor] = weight

	def setVisited(self):
		if self.color == 0:
			self.color = 1
		elif self.color == 1:
			self.color = 2
		else: self.color = 0

	def setDistance(self, dist):
		self.dist = dist
	
	def getWeight(self, neighbor):
		return self.adj[neighbor]
	
	def setPrevious(self, prev):
		self.prev = prev
	
	def getNeighbors(self):
		return list(zip([x.data for x in self.adj], list(self.adj.values())))

class Graph:
	
	def __init__(self):
		self.verticesNum = 0
		self.vertices = {}
	
	def __iter__(self):
		return iter(self.vertices.values())
	
	def getNeighbor_vertex(self, vertex):
		tmp = [tupl[0] for tupl in self.vertices[vertex].getNeighbors()]
		return [self.vertices[v] for v in tmp]
	
	def getVertices_str(self):
		for obj in self.vertices.values():
			print(f'{obj.data}: {obj.getNeighbors()}')
	
	def constructGraph(self, txt):
		source = open(txt, 'r')
		if not source:
			return
		while True:
			curr = source.readline().split()
			if not curr: break
			self.addEdge(curr[0], curr[1], int(curr[2]))
		source.close()
	
	def addVertex(self, data):
		if data in self.vertices:
			return
		new = Vertex(data)
		self.vertices[data] = new
		self.verticesNum += 1
	
	def addEdge(self, start, goal, weight = 0):
		if start not in self.vertices:
			self.addVertex(start)
		if goal not in self.vertices:
			self.addVertex(goal)
		self.vertices[start].addNeighbor(self.vertices[goal], weight)
	
	def removeVertex(self, vertex):
		if vertex not in self.vertices:
			return
		self.vertices.pop(vertex)
		self.verticesNum -= 1
		for vertices in self.vertices:
			for adj in self.vertices[vertices]:
				if adj[0] == vertex:
					self.vertices[vertices].remove((vertex, adj[1]))
	
	def dfs(self, start):
		visited, stack = set(), [start]
		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.add(vertex)
				vSet = {tupl[0] for tupl in self.vertices[vertex].getNeighbors()}
				stack.extend(vSet - visited)
		return visited
	
	def dfs_paths(self, start, goal):
		stack = [(start, [start])]
		while stack:
			(vertex, path) = stack.pop()
			vSet = {tupl[0] for tupl in self.vertices[vertex].getNeighbors()}
			for next in vSet - set(path):
				if next == goal:
					yield path + [next]
				else:
					stack.append((next, path + [next]))
	
	def bfs(self, start):
		visited, queue = set(), [start]
		while queue:
			vertex = queue.pop(0)
			if vertex not in visited:
				visited.add(vertex)
				vSet = {tupl[0] for tupl in self.vertices[vertex].getNeighbors()}
				stack.extend(vSet - visited)
		return visited
	
	def bfs_alg(self, start):
		for vertex in self.vertices.values():
			vertex.color = 0
			vertex.dist = float('inf')
			vertex.prev = None
		self.vertices[start].color = 1
		self.vertices[start].dist = 0
		self.vertices[start].prev = None
		queue = [self.vertices[start]]
		while queue:
			u = queue.pop(0)
			for v in self.getNeighbor_vertex(u.data):
				if v.color == 0:
					v.color = 1
					v.dist = u.dist + 1
					v.prev = u
					print(v.data, v.dist, v.prev.data)
					queue.append(v)
				u.color = 2
	
	def bfs_paths(self, start, goal):
		queue = [(start, [start])]
		while queue:
			(vertex, path) = queue.pop(0)
			vSet = {tupl[0] for tupl in self.vertices[vertex].getNeighbors()}
			for next in vSet - set(path):
				if next == goal:
					yield path + [next]
				else:
					queue.append((next, path + [next]))
	
	def findPath(self, start, goal, path = [], end = None):
		if not path:
			end = goal
		if start == goal:
			path.append(start)
		elif self.vertices[goal].prev == None:
			pass
		else:
			tmp = self.vertices[goal].prev.data
			self.findPath(start, tmp, path, end)
			path.append(goal)
		if end == path[-1]:
			return path
	
	def dijikstra(self, start):
		for vertex in self.vertices.values():
			vertex.setDistance(float('inf'))
			vertex.setPrevious(None)
		start.dist = 0
		done = set()
		queue = [obj for obj in self.vertices.values()]
		while queue:
			minValue = 0
			for i in range(len(queue)):
				if queue[i] not in done and queue[i].dist < queue[minValue].dist:
					minValue = i
			u = queue.pop(minValue)
			done.add(u)
			for v in self.getNeighbor_vertex(u.data):
				if v.dist > u.dist + u.getWeight(v):
					v.setDistance(u.dist + u.getWeight(v))
					v.setPrevious(u)

	def dijikstra_heap(self, start):
		for vertex in self.vertices.values():
			vertex.setDistance(float('inf'))
			vertex.setPrevious(None)
		start.dist = 0
		hqueue = Heap()
		hqueue.insertKey((start.data, start.dist))
		while not hqueue.isEmpty():
			u = self.vertices[hqueue.extractMin()[0]]
			for v in self.getNeighbor_vertex(u.data):
				if v.dist > u.dist + u.getWeight(v):
					v.setDistance(u.dist + u.getWeight(v))
					v.setPrevious(u)
					hqueue.insertKey((v.data, v.dist))

	def dijikstra_fib(self, start):
		for vertex in self.vertices.values():
			vertex.setDistance(float('inf'))
			vertex.setPrevious(None)
		start.dist = 0
		hqueue = FibonacciHeap()
		nodes = {start:hqueue.insert(start.data, start.dist)}
		while not hqueue.isEmptyF():
			u = self.vertices[hqueue.extractMinF().data]
			for v in self.getNeighbor_vertex(u.data):
				if v.dist > u.dist + u.getWeight(v):
					v.setDistance(u.dist + u.getWeight(v))
					v.setPrevious(u)
					try: hqueue.decreaseKey(nodes[v], v.dist)
					except KeyError: nodes.update({v:hqueue.insert(v.data, v.dist)})

test = Graph()
test.constructGraph('email-Eu-core-temporal.txt')
t0 = time.time()
test.dijikstra_fib(test.vertices['870'])
print(test.findPath('870', '771'))
t1 = time.time()
print(t1 - t0)

