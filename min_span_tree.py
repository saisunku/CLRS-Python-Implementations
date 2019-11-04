# Prim's algorithm for building a minimum spanning tree

import copy
import math

# Node object
class node(object):
	def __init__(self):
		self.num = -1		# Vertex index
		self.adj = []		# Adjacency list of integers that correspond to adjacent nodes
		self.weight = []	# List of weights for the edges in the same order as adjacency list
		self.key = float('Inf')	# Key for priority heap
		self.pred = None	# Predecessor node 

	def __eq__(self, other):	# Equality method needed for comparing nodes after deep copy
		return self.num == other.num

# Graph object
class graph(object):
	def __init__(self, nodes, root):
		self.root = root
		self.nodes = nodes	# List of nodes
		
		for idx, cur_node in enumerate(nodes):	# The vertex index for each node is the position of the node in the list
			if not isinstance(cur_node, node):
				raise TypeError
			cur_node.num = idx

	def get_keys(self):		# List of all keys in the graph. For debugging.
		keys = []
		for node in self.nodes:
			keys.append(node.key)
		return keys


# Min priority queue of nodes that operates on a key that can be arbitrarily set
class min_priority_queue(object):
	def __init__(self, A):
		self.heap = copy.deepcopy(A)    # Need to have own copy so that the graph nodes are unaffected by extract_min 
		self.heap_size = len(self.heap)
        
		for j in range(math.floor(self.heap_size/2)-1, -1, -1):
			self.min_heapify(j)

	def get_nums(self):
		nums = [] 
		for node in self.heap:
			nums.append(node.num)
		return nums

	def left(self, k):
		return (k << 1) + 1
    
	def right(self, k):
		return (k << 1) + 2
    
	def parent(self, k):
		return math.ceil(k/2) - 1
    
	def min_heapify(self, k):
		smallest = k
		if self.left(k) < self.heap_size and self.heap[self.left(k)].key < self.heap[smallest].key:
			smallest = self.left(k)
        
		if self.right(k) < self.heap_size and self.heap[self.right(k)].key < self.heap[smallest].key:
			smallest = self.right(k)
            
		if smallest != k:
			# print('swapping')
			tmp = self.heap[k]
			self.heap[k] = self.heap[smallest]
			self.heap[smallest] = tmp
            
			self.min_heapify(smallest)
            
	def extract_min(self):
		# print(self.get_nums())
		to_return = self.heap[0]

		self.heap[0] = self.heap[self.heap_size-1]
		del self.heap[self.heap_size-1]
		self.heap_size -= 1

		self.min_heapify(0)
		
		# print(self.get_nums())
		return to_return
    
	def decrease_key(self, node_num, new_val): 
        # Decrease the key value of the node with number node_num to new_val
	# Need to use node_num to identify the node here because the ordering of the nodes in the graph and heap are not the same
		k = None
		for idx, node in enumerate(self.heap):
			if node.num == node_num:
				k = idx
		# print('k, node_num '+str(k)+' '+str(node_num))
		assert new_val < self.heap[k].key   # Make sure new value is smaller than the current value
        
		self.heap[k].key = new_val
		while self.parent(k) > -1 and self.heap[self.parent(k)].key > new_val:
			tmp = self.heap[self.parent(k)]
			self.heap[self.parent(k)] = self.heap[k]
			self.heap[k] = tmp

			k = self.parent(k)


# Prim's algorithm for minimum spanning tree
def prim_mst(graph, root=None):
	if root == None:
		root = graph.root
	
	# Initialize the nodes
	for node in graph.nodes:
		node.pred = None
		node.key = float('Inf')

	root.key = 0
	heap = min_priority_queue(graph.nodes)

	while heap.heap_size > 0:
		cur_node = heap.extract_min()
		# print('cur node: '+str(cur_node.num))
		# print(graph.get_keys())

		for node, weight in zip(cur_node.adj, cur_node.weight):
			if graph.nodes[node] in heap.heap and graph.nodes[node].key > weight:
				graph.nodes[node].key = weight
				graph.nodes[node].pred = cur_node
				heap.decrease_key(graph.nodes[node].num, weight)
		
		# print(graph.get_keys())
	

# Slightly modified version of the graph from Pg 635
# Modify w(0, 7) = 20 and w(7, 8) = 21 to force the same MST as the textbook
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node(); n5 = node(); n6 = node(); n7 = node(); n8 = node();
n0.adj = [1, 7]; n0.weight = [4, 20];
n1.adj = [2, 7]; n1.weight = [8, 11];
n2.adj = [3, 5, 8, 1]; n2.weight = [7, 4, 2, 8];
n3.adj = [2, 4, 5]; n3.weight = [7, 9, 14];
n4.adj = [3, 5]; n4.weight = [9, 10];
n5.adj = [2, 3, 4, 6]; n5.weight = [4, 14, 10, 2];
n6.adj = [5, 7, 8]; n6.weight = [2, 1, 6];
n7.adj = [0, 1, 6, 8]; n7.weight = [20, 11, 1, 21];
n8.adj = [2, 6, 7]; n8.weight = [2, 6, 21];

G = graph([n0, n1, n2, n3, n4, n5, n6, n7, n8], n0)

# First test the min priority queue
n0.key = 54; n1.key = 28; n2.key = 45; n3.key = 15; n4.key = 36; n5.key = 12; n6.key = 32; n7.key = 93; n8.key = float('Inf');

heap = min_priority_queue(G.nodes)

# Check that the heap property is maintained for all nodes
for j in range(heap.heap_size):
    if heap.left(j) < heap.heap_size:
        assert heap.heap[heap.left(j)].key >= heap.heap[j].key
    if heap.right(j) < heap.heap_size:
        assert heap.heap[heap.right(j)].key >= heap.heap[j].key
 
# Test extract_min
min_node = heap.extract_min()
assert min_node.key == 12
min_node = heap.extract_min()
assert min_node.key == 15
min_node = heap.extract_min()
assert min_node.key == 28

# Test decrease_key
heap.decrease_key(8, -1)
min_node = heap.extract_min()
assert min_node.key == -1

# Now find the minimum spanning tree
prim_mst(G)

assert n1.pred == n0
assert n8.pred == n2
assert n5.pred == n2
assert n7.pred == n6
assert n4.pred == n3

