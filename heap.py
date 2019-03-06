class Heap:

	def __init__(self, arr = []):
		if not arr:
			arr.append(None)
		if arr[0] != None:
			arr.insert(0, None)
		self.nodes = arr
	
	def minHeapify(self, index):
		left = 2 * index
		right = (2 * index) + 1
		minimum = 0
		if left <= len(self.nodes) - 1 and self.nodes[left][1] < self.nodes[index][1]:
			minimum = left
		else: minimum = index
		if right <= len(self.nodes) - 1 and self.nodes[right][1] < self.nodes[minimum][1]:
			minimum = right
		if minimum != index:
			tmp = self.nodes[index]
			self.nodes[index] = self.nodes[minimum]
			self.nodes[minimum] = tmp
			self.minHeapify(minimum)
	
	def buildHeap_min(self):
		for i in range(len(self.nodes)//2, 0, -1):
			self.minHeapify(i)
	
	def isEmpty(self):
		return len(self.nodes) == 1

	def extractMin(self):
		if self.isEmpty():
			return
		minimum = self.nodes[1]
		self.nodes[1] = self.nodes[-1]
		self.nodes.pop(-1)
		self.minHeapify(1)
		return minimum

	def insertKey(self, new):
		self.nodes.append(new)
		i = len(self.nodes) - 1
		while i > 1 and self.nodes[i // 2][1] > self.nodes[i][1]:
			tmp = self.nodes[i]
			self.nodes[i] = self.nodes[i // 2]
			self.nodes[i // 2] = tmp
			i = i // 2
		return i