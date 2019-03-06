class Node:

	def __init__(self, data, key):
		self.data = data
		self.parent = None
		self.children = []	
		self.mark = False
		self.key = key
		self.degree = 0

class FibonacciHeap:

	def __init__(self):
		self.root = []
		self.n = 0
		self.min = None

	def insert(self, new, key):
		node = Node(new, key)
		self.root.append(node)
		if self.min == None or key < self.min.key:
			self.min = node
		self.n += 1
		return node

	def extractMinF(self):
		z = self.min
		if z != None:
			self.root.extend(z.children)
			index = self.root.index(z)
			curr = None
			if index == len(self.root) - 1:
				curr = self.root[0]
			else: curr = self.root[index + 1]
			self.root.remove(z)
			if len(self.root) == 0:
				self.min = None
			else:
				self.min = curr
				self.__consolidate()
			self.n -= 1
		return z

	def __link(self, y, x):
		self.root.remove(y)
		x.children.append(y)
		y.mark = False
		x.degree += 1
		y.parent = x

	def __consolidate(self):
		A = [None] * self.n
		for w in self.root:
			d = w.degree
			while A[d] != None:
				y = A[d]
				if w.key > y.key:
					tmp = w
					w, y = y, tmp
				self.__link(y, w)
				A[d] = None
				d += 1
			A[d] = w
		self.min = None
		for i in A:
			if i is not None:
				if self.min == None:
					self.min = i
				elif i.key < self.min.key:
					self.min = i

	def isEmptyF(self):
		return self.n == 0

	def decreaseKey(self, x, key):
		x.key = key
		y = x.parent
		if y is not None and x.key < y.key:
			self.__cut(x, y)
			self.__cascadingCut(y)
		if x.key < self.min.key:
			self.min = x

	def __cut(self, x, y):
		y.children.remove(x)
		y.degree -= 1
		x.parent = None
		x.mark = False
		self.root.append(x)

	def __cascadingCut(self, y):
		z = y.parent
		if z != None:
			if y.mark == False:
				y.mark == True
			else:
				self.__cut(y, z)
				self.__cascadingCut(z)

# test = Fibonacci()
# test.insert('a', 33333)
# test.insert('ae', 133)
# test.insert('aaa', 323)
# test.insert('a2', 334)
# test.insert('aww', 3311)

# print(test.extractMinF().data)
# print(test.extractMinF().data)
# print(test.extractMinF().data)
# print(test.extractMinF().data)
# print(test.extractMinF().data)
