# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 13:59:50 2019

@author: Sai
"""

class min_priority_queue(object):
    def __init__(self, A):
        self.heap = copy.deepcopy(A)    # Need to have own copy so that the array is unaffected when extract_min is run
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
#        print(k)
#        print(self.heap)
        smallest = k
        if self.left(k) < self.heap_size and self.heap[self.left(k)] < self.heap[smallest]:
            smallest = self.left(k)
        # Do NOT use elif in the line below - did it twice so far
        if self.right(k) < self.heap_size and self.heap[self.right(k)] < self.heap[smallest]:
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
#        print('min heapifying')
        self.min_heapify(0)
        
        return to_return
    
    def decrease_key(self, k, new_val):    
        # Decrease the key value of the k-th element to new_val
        
#        Recursive version         
#        if self.parent(k) > -1 and new_val < self.heap[self.parent(k)]:
#            # Swap with the parent
#            tmp = self.heap[self.parent(k)]
#            self.heap[self.parent(k)] = new_val
#            self.heap[k] = tmp
#            
#            # Recurse
#            self.decrease_key(self.parent(k), new_val)

        
#       Iterative versions are always better..
        assert new_val < self.heap[k]   # Make sure new value is smaller than the current value
        
        self.heap[k] = new_val
        while self.parent(k) > -1 and self.heap[self.parent(k)] > new_val:
            tmp = self.heap[self.parent(k)]
            self.heap[self.parent(k)] = new_val
            self.heap[k] = tmp
            
            k = self.parent(k)
            
    def push(self, new_val):
        # To push a new value, we add it at the end and let it float up
        self.heap_size += 1
        self.heap[self.heap_size-1] = float('inf')
        
        self.decrease_key(self.heap_size-1, new_val)
        
        
    def draw_heap(self, spacing=2, width=2):
        # Draws the heap
        
        # Number of levels = 1 + height of tree
        num_levels = math.floor(math.log(self.heap_size+1,2))+1
        print('heap size '+str(self.heap_size+1))
        print('num levels '+str(num_levels))
#        print(self.heap)
        
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
                    str_level += fmt.format(self.heap[2**height-1+val])   # Then add the number
                    str_level += ' '*int(spacing_array[height])    # And the space between the numbers
                else:
                    str_level += 'X'*width   # If outside the heap, show 'X'
                    str_level += ' '*int(spacing_array[height])
            str_list[height] = str_level

        # Now print
        for height in range(num_levels):
            print(str_list[height]+'\n')
            
        return str_list

        
# First let's test the heap
array = [1, 3, 9, 10, 14, 8, 2, 4, 16, 7, 36, 7, 8, 99, 12, 5, 43, 1, 45, 4, 22, 67, 8, 11, 48, 9, 36, 46, 77, 99]
A = min_priority_queue(array)

# Check that the heap property is maintained for all nodes
for j in range(A.heap_size):
    if A.left(j) < A.heap_size:
        assert A.heap[A.left(j)] >= A.heap[j]
    if A.right(j) < A.heap_size:
        assert A.heap[A.right(j)] >= A.heap[j]
        
# Now test extract_min
#print(A.heap)
assert A.extract_min() == min(array)
array.remove(min(array))
#print(A.heap)
assert A.extract_min() == min(array)
array.remove(min(array))
assert A.extract_min() == min(array)
array.remove(min(array))
assert A.extract_min() == min(array)
array.remove(min(array))
assert A.extract_min() == min(array)
array.remove(min(array))
assert A.extract_min() == min(array)
array.remove(min(array))
assert A.extract_min() == min(array)

# Now test push
A.draw_heap()
A.push(-1)
A.draw_heap()
# Check that the heap property is maintained for all nodes
for j in range(A.heap_size):
    if A.left(j) < A.heap_size:
        assert A.heap[A.left(j)] >= A.heap[j]
    if A.right(j) < A.heap_size:
        assert A.heap[A.right(j)] >= A.heap[j]

assert A.extract_min() == -1    # Because the pushed value is negative and all other numbers in the heap are positive

A.draw_heap()
A.push(10)
A.draw_heap()
# Check that the heap property is maintained for all nodes
for j in range(A.heap_size):
    if A.left(j) < A.heap_size:
        assert A.heap[A.left(j)] >= A.heap[j]
    if A.right(j) < A.heap_size:
        assert A.heap[A.right(j)] >= A.heap[j]