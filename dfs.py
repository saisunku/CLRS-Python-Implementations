# Depth-first search and related graph algorithms

# Data structures for representing graphs

# Node object
class node(object):
	def __init__(self):
		self.num = -1		# Vertex index
		self.adj = []		# Adjacency list of integers that correspond to adjacent nodes
		self.pred = None	# Predecessor node 
		self.visited = False	# Boolean indicating whether the node has been visited
		self.discovered = -1	# Time when the node is discovered
		self.finished = -1	# Time when the node is finished

# Graph object
class graph(object):
	def __init__(self, nodes, root):
		self.root = root
		self.nodes = nodes	# List of nodes
		
		for idx, cur_node in enumerate(nodes):	# The vertex index for each node is the position of the node in the list
			if not isinstance(cur_node, node):
				raise TypeError
			cur_node.num = idx

		self.time = 0		# Global time used to mark when the nodes are discovered and finished


# First, a simple iterative version using a Python list as a stack. 
# Note: this version cannot compute discovered and finished times 
def DFS_iterative(graph, root=None):
	if root == None:
		root = graph.root

	# Initialize the nodes
	for node in graph.nodes:
		node.pred = None
		node.visited = False

	node_stack = []
	node_stack.append(root)
	root.visited = True
	# graph.time += 1			# To maintain consistency with the recursive version
	# root.discovered = graph.time

	while len(node_stack) > 0:
		cur_node = node_stack.pop()
		for neighbor in cur_node.adj:
			if graph.nodes[neighbor].visited == False:
				graph.nodes[neighbor].pred = cur_node
				node_stack.append(graph.nodes[neighbor])
				graph.nodes[neighbor].visited = True
	

# Test case from Pg 605
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node(); n5 = node();
n0.adj = [1, 3]
n1.adj = [4]
n2.adj = [4, 5]
n3.adj = [1]
n4.adj = [3]
n5.adj = [5]

G = graph([n0, n1, n2, n3, n4, n5], root=n0)
DFS_iterative(G)

assert n0.visited == True
assert n3.visited == True
assert n5.visited == False
assert n2.visited == False

G = graph([n0, n1, n2, n3, n4, n5], root=n2)
DFS_iterative(G)

assert n0.visited == False
assert n1.visited == True
assert n2.visited == True
assert n3.visited == True
assert n4.visited == True
assert n5.visited == True

# Iterative version that also computes the discovered and finished times
# While it works, it is much more inefficient than the recursive case
def DFS_iterative_disc_finish_times(graph, root=None):
	if root == None:
		root = graph.root

	# Initialize the nodes
	for node in graph.nodes:
		node.pred = None
		node.visited = False
		node.discovered = -1
		node.finished = -1
	graph.time = 0	

	node_stack = []
	node_stack.append(root)
	root.visited = True

	graph.time += 1
	root.discovered = graph.time

	while len(node_stack) > 0:
		cur_node = node_stack[-1]	# Peek the stack
		if cur_node.discovered == -1:	# Discovered time is added only the first time the node is peeked
			graph.time += 1
			cur_node.discovered = graph.time
	
		# Check if this cur_node should be popped
		should_pop = True
		for neighbor in cur_node.adj:
			if graph.nodes[neighbor].visited == False:
				should_pop = False

		if should_pop:
			graph.time += 1
			cur_node.finished = graph.time
			node_stack.pop()

		# If not, process the node
		for neighbor in cur_node.adj:
			if graph.nodes[neighbor].visited == False:
				graph.nodes[neighbor].pred = cur_node
				node_stack.append(graph.nodes[neighbor])
				graph.nodes[neighbor].visited = True

		
G = graph([n0, n1, n2, n3, n4, n5], root=n0)
DFS_iterative_disc_finish_times(G)

discovered_array = [-1]*len(G.nodes)
finished_array = [-1]*len(G.nodes)
for idx, cur_node in enumerate(G.nodes):
	discovered_array[idx] = cur_node.discovered
	finished_array[idx] = cur_node.finished

print('iterative discovered: '+str(discovered_array))
print('iterative finished: '+str(finished_array))


# Recrusive version Pg 604
def DFS(graph):
	# Initialize the nodes
	for node in graph.nodes:
		node.pred = None
		node.visited = False
		node.discovered = -1
		node.finished = -1
	graph.time = 0

	for node in graph.nodes:
		if node.visited == False:
			DFS_visit(graph, node)

def DFS_visit(graph, cur_node):
	graph.time += 1
	cur_node.discovered = graph.time
	cur_node.visited = True

	for neighbor in cur_node.adj:
		if graph.nodes[neighbor].visited == False:
			graph.nodes[neighbor].pred = cur_node
			DFS_visit(graph, graph.nodes[neighbor])

	graph.time += 1
	cur_node.finished = graph.time	
			

# Test case from Pg 605
DFS(G)

discovered_array = [-1]*len(G.nodes)
finished_array = [-1]*len(G.nodes)
for idx, cur_node in enumerate(G.nodes):
	discovered_array[idx] = cur_node.discovered
	finished_array[idx] = cur_node.finished

print('recursive discovered: '+str(discovered_array))
print('recursive finished: '+str(finished_array))

assert discovered_array == [1, 2, 9, 4, 3, 10]
assert finished_array == [8, 7, 12, 5, 6, 11]


# Topological sort of a DAG with DFS
# Returns an array that is an arrangement of the initial nodes sorted topologically
def topo_sort(graph):
	DFS(graph)

	finished_array = [-1]*len(graph.nodes)
	for idx, node in enumerate(graph.nodes):
		finished_array[idx] = node.finished

	topo_sort_list = []
	for j in range(len(finished_array)):
		min_idx = finished_array.index(min(finished_array))
		topo_sort_list.append(min_idx)
		finished_array[min_idx] = float('Inf')

	return topo_sort_list[::-1]

# Test case based on Pg 613 of CLRS
n0 = node(); n1 = node(); n2 = node(); n3 = node(); n4 = node(); n5 = node(); n6 = node(); n7 = node(); n8 = node(); 
n0.adj = [1, 7]; n1.adj = [2, 7]; n2.adj = [5]; n3.adj = [2, 4]; n4.adj = [5]; n5.adj = []; n6.adj = [7];

G = graph([n0, n1, n2, n3, n4, n5, n6, n7, n8], root=n0)

print('Topological sort: '+str(topo_sort(G)))

