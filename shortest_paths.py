# Single source shortest path algorithms

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


# Relaxation function for Bellman-Ford algorithm
def relax_bf(u, v, weight):
	if v.key > u.key + weight:
		v.key = u.key + weight
		v.pred = u
	

# Bellman-Ford algorithm
def bellman_ford(graph, source=None):
	if source == None:
		source = graph.root
	
	source.key = 0

	for j in range(len(graph.nodes)-1):	# Relax all edges V-1 times
		for node in graph.nodes:
			for idx, adj_node in enumerate(node.adj):
				relax_bf(node, graph.nodes[adj_node], node.weight[idx])

	for node in graph.nodes:	# Check for negative cycles by testing if the weights change after another relaxation
		for idx, adj_node in enumerate(node.adj):
			if graph.nodes[adj_node].key > node.key + node.weight[idx]:
				return False

	return True

# Test case from Pg 652
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node();
n0.adj = [1, 3]; n0.weight = [6, 7];
n1.adj = [2, 3, 4]; n1.weight = [5, 8, -4];
n2.adj = [1]; n2.weight = [-2];
n3.adj = [2, 4]; n3.weight = [-3, 9];
n4.adj = [0, 2]; n4.weight = [2, 7];

G = graph([n0, n1, n2, n3, n4], root=n0)

bellman_ford(G)

assert G.get_keys() == [0, 2, 4, 7, -2]


# Simple test case with a negative cycle
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node();
n0.adj = [1, 4]; n0.weight = [3, 2];
n1.adj = [2]; n1.weight = [6];
n2.adj = [3, 4]; n2.weight = [-7, 5];
n3.adj = [0]; n3.weight = [-3];
n4.adj = []; n4.weight = [];

G = graph([n0, n1, n2, n3, n4], root=n0)

assert bellman_ford(G) == False



# Min priority queue of nodes that operates on a key that can be arbitrarily set - for Dijkstra's algorithm
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


def relax_dijkstra(u, v, weight, heap):
	# Relaxation function for Dijkstra's algorithm which also calls the 'decrease_key' function at the end
	# print('v. key, u.key, weight '+str(v.key)+' '+str(u.key)+' '+str(weight))
	if v.key > u.key + weight:
		v.key = u.key + weight
		v.pred = u
		heap.decrease_key(v.num, u.key + weight)


# Dijkstra's algorithm
def dijkstra(graph, root=None):
	if root == None:
		root = graph.root

	root.key = 0
	heap = min_priority_queue(graph.nodes)

	while heap.heap_size > 0:
		cur_node = heap.extract_min()
		# print('cur node '+str(cur_node.num))

		for node, weight in zip(cur_node.adj, cur_node.weight):
			# print(node, weight)
			relax_dijkstra(cur_node, graph.nodes[node], weight, heap)


# Graph from Pg 659 of CLRS
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node();
n0.adj = [1, 3]; n0.weight = [10, 5];
n1.adj = [2, 3]; n1.weight = [1, 2];
n2.adj = [4]; n2.weight = [4];
n3.adj = [1, 2, 4]; n3.weight = [3, 9, 2];
n4.adj = [0, 2]; n4.weight = [7, 6]

G = graph([n0, n1, n2, n3, n4], root=n0)

dijkstra(G)

assert G.get_keys() == [0, 8, 9, 5, 7]



