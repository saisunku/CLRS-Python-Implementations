# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:44:32 2019

@author: Sai
"""

import math
import copy

# Huffman codes for data compression
# Pg 428 CLRS

# First the data structure for holding the Huffman code
class huffman_node(object):
    # Node object has the sum of frequency all leaves under the node
    # It's children can either be other nodes or leaves
    def __init__(self, freq):
        self.freq = freq
        self.left = None
        self.right = None
        
    # Equality operator is useful for testing
    def __eq__(self, other):
        if not isinstance(other, huffman_node):
            return NotImplemented
        else:
            return self.freq == other.freq
        
class huffman_leaf(object):
    # Leaf object has a character and an associated frequency
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.parent = None
        
    # Equality operator is useful for testing
    def __eq__(self, other):
        if not isinstance(other, huffman_leaf):
            return NotImplemented
        else:
            return self.freq == other.freq and self.char == other.char


class huffman_tree(object):
    # Huffman tree object
    def __init__(self, char_freq_dict):
        # When the tree is initialized we have a bunch of disconnected leaves
        self.root = None
        self.leaves = []
        for char in iter(char_freq_dict):
            new_leaf = huffman_leaf(char, char_freq_dict[char])
            self.leaves.append(new_leaf)
            
    def build_code(self):
        self.min_queue = min_queue_huffman(self.leaves)
        num_leaves = len(self.leaves)
        for j in range(num_leaves-1):
            x = self.min_queue.extract_min()
            y = self.min_queue.extract_min()
            
            z = huffman_node(x.freq + y.freq)
            z.left = x
            z.right = y
            
            self.min_queue.push_node(z)
            # print(z.freq)
        
        self.root = self.min_queue.extract_min()
        
        # Traverse the tree and build a character-to-code dictionary
#        cur_node = self.root
        
    def encode(self, message):
        assert self.root != None        # Make sure the build_code function was run
        encoded_str = ''
        pass            
        
        
    def decode(self, message):
        assert self.root != None        # Make sure the build_code function was run
        decoded_str = ''
        cur_char = 0                    # Pointer to the current character being read
        while cur_char < len(message):
            # print('root')
            cur_node = self.root
            while isinstance(cur_node, huffman_node):
                if message[cur_char] == '0':
                    # print('0')
                    cur_node = cur_node.left
                    cur_char += 1
                elif message[cur_char] == '1':
                    # print('1')
                    cur_node = cur_node.right
                    cur_char += 1
                else:
                    print('unrecognized char')
                    break
            decoded_str += cur_node.char
            # print(decoded_str)
        
        return decoded_str
            

class min_queue_huffman(object):
    # A min priority queue for nodes in Huffman code
    def __init__(self, A):
        self.heap = copy.deepcopy(A)        # Need to have own copy so that the originial array is unaffected when extract_min is run
        self.heap_size = len(self.heap)
        
        for j in range(math.floor(self.heap_size/2)-1, -1, -1):
            self.min_heapify(j)
    
    def left(self, k):
        return (k << 1) + 1
    
    def right(self, k):
        return (k << 1) + 2
    
    def parent(self, k):
        return math.ceil(k/2) - 1
    
    def min_heapify(self, k):
        smallest = k
        if self.left(k) < self.heap_size and self.heap[self.left(k)].freq < self.heap[smallest].freq:
            smallest = self.left(k)
        # Do NOT use elif in the line below - did it twice so far
        if self.right(k) < self.heap_size and self.heap[self.right(k)].freq < self.heap[smallest].freq:
            smallest = self.right(k)
            
        if smallest != k:
            tmp = self.heap[k]
            self.heap[k] = self.heap[smallest]
            self.heap[smallest] = tmp
            
            self.min_heapify(smallest)
            
    def extract_min(self):
        to_return = self.heap[0]
        self.heap[0] = self.heap[self.heap_size-1]
        self.heap_size -= 1
        self.min_heapify(0)
        
        return to_return
    
    
    def push_node(self, new_node):
        # To push in a new Huffman node, add it at the end and let it float up
        assert isinstance(new_node, huffman_node) == True     # Can only push nodes, not leaves
        # print(new_node.freq)
        self.heap_size += 1
        self.heap[self.heap_size-1] = new_node

        # If the frequency of the new node is larger than its parent, then we are done
        if new_node.freq > self.heap[self.parent(self.heap_size-1)].freq:
            # print('passed')
            pass
        else:
            self.decrease_key(self.heap_size-1, new_node)

        
    def decrease_key(self, k, new_node):
        # Auxillary function for push
        # Puts the new node in the correct place
        while self.parent(k) > -1 and self.heap[self.parent(k)].freq > new_node.freq:
            tmp = self.heap[self.parent(k)]
            self.heap[self.parent(k)] = new_node
            self.heap[k] = tmp
            
            k = self.parent(k)
    
                
    def draw_heap(self, spacing=2, width=2):
        # Draws the heap
        
        # Number of levels = 1 + height of tree
        num_levels = math.floor(math.log(self.heap_size,2))+1
        print('heap size '+str(self.heap_size))
        print('num levels '+str(num_levels))
        # print(self.heap)
        
        # Calculate the spacing and offset arrays
        spacing_array = [0]*num_levels
        offset_array = [0]*num_levels
        
        spacing_array[-1] = spacing         # Spacing at the last level is set to a fixed value
        offset_array[-1] = 0                # Last level has no offset
        
        # Now iterate backwards and calculate spacing and offsets for all levels
        for j in range(num_levels-2, -1, -1):
            spacing_array[j] = spacing_array[j+1]*2 + width     # Spacing of the m-th level is twice the spacing of the m+1-th level
            offset_array[j] = offset_array[j+1] + spacing_array[j+1]/2 + width  # Offset of m-th level = offset of previous level + spacing of previous level/2
        
        # Iterate backwards again and construct the string at each level
        str_list = ['']*num_levels
        fmt = '{:^'+str(width)+'d}'
        for height in range(num_levels-1, -1, -1):
            str_level = ' '*int(offset_array[height])         # First add the offset
            for val in range(2**height):
                if 2**height-1+val < self.heap_size:
                    str_level += fmt.format(self.heap[2**height-1+val].freq)   # Then add the number
                    str_level += ' '*int(spacing_array[height])    # And the space between the numbers
                else:
                    str_level += 'X'*width   # If outside the heap, show 'X'
                    str_level += ' '*int(spacing_array[height])
            str_list[height] = str_level

        # Now print
        for height in range(num_levels):
            print(str_list[height]+'\n')
            
        return str_list

# First test the Huffman node and leaf
n1 = huffman_node(10)
assert n1.freq == 10
leaf1 = huffman_leaf('a', 10)
assert leaf1.char == 'a'
assert leaf1.freq == 10
leaf2 = huffman_leaf('b', 20)
assert leaf2.char == 'b'
assert leaf2.freq == 20

# Now test the Huffman tree object
char_freq_dict = {'a':10, 'b':20, 'c':30, 'd':40}
htree = huffman_tree(char_freq_dict)
assert htree.leaves[0] == leaf1
assert htree.leaves[1] == leaf2
assert htree.leaves[2].freq == 30
assert htree.leaves[3].char == 'd'

# Make a list of leaves to test the min_queue_huffman class
leaves = [huffman_leaf('a', 10), huffman_leaf('b', 20), huffman_leaf('c', 30), huffman_leaf('d', 40), huffman_leaf('e', 50), huffman_leaf('f', 60), huffman_leaf('g', 70)]
min_queue = min_queue_huffman(leaves)
min_queue.draw_heap()

assert min_queue.extract_min() == leaf1
assert min_queue.extract_min() == leaf2
min_queue.draw_heap()

node10 = huffman_node(10)
node20 = huffman_node(20)
min_queue.push_node(node10)
min_queue.draw_heap()
min_queue.push_node(node20)
min_queue.draw_heap()
assert min_queue.extract_min() == node10
assert min_queue.extract_min() == node20


# Now we are ready to test the code building
# Test case from Pg 429 CLRS
char_freq_dict = {'a':45, 'b':13, 'c':12, 'd':16, 'e':9, 'f':5}
htree = huffman_tree(char_freq_dict)
htree.build_code()
hroot = htree.root
assert hroot.freq == 100
assert hroot.left.char == 'a'
assert hroot.left.freq == char_freq_dict['a']
assert hroot.right.left.left.char == 'c'
assert hroot.right.left.left.freq == char_freq_dict['c']
assert hroot.right.right.left.right.char == 'e'
assert hroot.right.right.left.right.freq == char_freq_dict['e']

# Test case from https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/
char_freq_dict = {'a':5, 'b':9, 'c':12, 'd':13, 'e':16, 'f':45}
htree = huffman_tree(char_freq_dict)
htree.build_code()
hroot = htree.root
assert hroot.freq == 100
assert hroot.left.char == 'f'
assert hroot.left.freq == char_freq_dict['f']
assert hroot.right.left.left.char == 'c'
assert hroot.right.left.left.freq == char_freq_dict['c']
assert hroot.right.right.left.right.char == 'b'
assert hroot.right.right.left.right.freq == char_freq_dict['b']


# Now test decoding
char_freq_dict = {'a':45, 'b':13, 'c':12, 'd':16, 'e':9, 'f':5}
htree = huffman_tree(char_freq_dict)
htree.build_code()

encoded_str = '001011101'
assert htree.decode(encoded_str) == 'aabe'

encoded_str = '110011011111001010'
assert htree.decode(encoded_str) == 'fedcba'

encoded_str = '010110011111011100110011011111001010'
assert htree.decode(encoded_str) == 'abcdeffedcba'