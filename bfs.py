from queue import Queue

# Basic graph algorithms - Breadth-first search

# Data structures for representing graphs

# Node object
class node(object):
	def __init__(self):
		self.num = -1			# Vertex index
		self.adj = []			# Adjacency list of integers that correspond to adjacent nodes
		self.depth = float('Inf')	# Depth of the node from root
		self.pred = None		# Predecessor node for BFS
		self.visited = False		# Boolean indicating whether the node has been visited

# Graph object
class graph(object):
	def __init__(self, nodes, root):
		self.root = root
		self.root.depth = 0
		self.nodes = nodes	# List of nodes
		
		for idx, cur_node in enumerate(nodes):	# The vertex index for each node is the position of the node in the list
			if not isinstance(cur_node, node):
				raise TypeError
			cur_node.num = idx

# Breadth-first search - Pg 595
def BFS(graph, root=None):
	if root == None:
		root = graph.root

	root.visited = True
	root.pred = None
	root.depth = 0

	node_queue = Queue()
	node_queue.put(root)

	while not node_queue.empty():
		cur_node = node_queue.get()
		cur_node.visited = True

		for neighbor in cur_node.adj:
			# print(neighbor)
			if graph.nodes[neighbor].visited == False:
				node_queue.put(graph.nodes[neighbor])

				# For a node to be marked as visited, it needs a predecessor and depth
				graph.nodes[neighbor].pred = cur_node
				graph.nodes[neighbor].depth = cur_node.depth + 1
				graph.nodes[neighbor].visited = True
			

# Print path - Make sure you run BFS before running this
# Pg 601 CLRS
def print_path(graph, node):
	if node.num == graph.root.num:
		print(graph.root.num)
	elif node.pred == None:
		print('No path from root to node '+str(node.num))
	else:
		print_path(graph, node.pred)
	print(str(node.num))



# Test BFS - test case from Pg 590 CLRS
n0 = node(); n0.adj = [1, 4];
n1 = node(); n1.adj = [0, 4, 2, 3];
n2 = node(); n2.adj = [1, 3];
n3 = node(); n3.adj = [1, 4, 2];
n4 = node(); n4.adj = [3, 0, 1];

G = graph([n0, n1, n2, n3, n4], root=n2)

BFS(G)

assert n2.depth == 0
assert n1.depth == 1
assert n4.depth == 2
assert n0.depth == 2

print_path(G, n4)
print('\n')
print_path(G, n0)

