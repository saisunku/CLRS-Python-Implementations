# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 12:42:29 2019

@author: Sai
"""
import math
import random

# 9/8/2019
# Insertion sort - Pg 18 CLRS
def insertion_sort(array):
    for (idx, key) in enumerate(array[1:]):
        i = idx # Even though i and idx are equal, key = a[i+1]
        while i > -1 and array[i] > key:
            array[i+1] = array[i]
            i = i - 1
        array[i+1] = key
    return array
        
array = [5, 2, 4, 6, 1, 3]
#print(insertion_sort(array))
assert insertion_sort(array) == [1, 2, 3, 4, 5, 6]
array = [31, 41, 59, 26, 41, 58]
#print(insertion_sort(array))
assert insertion_sort(array) == [26, 31, 41, 41, 58, 59]

# Insertion sort in nonascending order - Pg 22 CLRS - Exercise 2.1.2
def insertion_sort_descending(array):
    for (idx, key) in enumerate(array[1:]):
        i = idx # Even though i and idx are equal, key = a[i+1]
        while i > -1 and array[i] < key:
            array[i+1] = array[i]
            i = i - 1
        array[i+1] = key
    return array

array = [5, 2, 4, 6, 1, 3]
#print(insertion_sort_descending(array))
assert insertion_sort_descending(array) == [6, 5, 4, 3, 2, 1]
array = [31, 41, 59, 26, 41, 58]
#print(insertion_sort_descending(array))
assert insertion_sort_descending(array) == [59, 58, 41, 41, 31, 26]

# Mergesort - Pg 31-34 CLRS
# First write the merge function and show that it works
def merge(array, p, q, r):
    left = array[p:q+1]
    right = array[q+1:r+1]
    left.append(float('inf'))
    right.append(float('inf'))
#    print(left, right)
    i = 0; j = 0;
    for k in range(r-p+1):
        if left[i] <= right[j]:
            array[k+p] = left[i]
            i += 1
        else:
            array[k+p] = right[j]
            j += 1
    return array
            
array = [1, 2, 4, 7, 3, 6, 9, 12]
#print(merge(array, 0, 3, len(array)-1))
assert merge(array, 0, 3, len(array)-1) == [1, 2, 3, 4, 6, 7, 9, 12]

# The merge sort itself is pretty simple
def merge_sort(array, p=0, r=None):
    if r == None:
        r = len(array)-1
    if p < r:
        q = math.floor((r+p)/2)
        merge_sort(array, p, q)
        merge_sort(array, q+1, r)
#        print('p, r: ', p, r)
        merge(array, p, q, r)
#        print(array)
    return array

array = [5, 2, 4, 6, 1, 3]
#print(merge_sort(array))
assert merge_sort(array) == [1, 2, 3, 4, 5, 6]
array = [31, 41, 59, 26, 41, 58]
#print(merge_sort(array))
assert merge_sort(array) == [26, 31, 41, 41, 58, 59]


# Heapsort - Chapter 6 CLRS

# First define heap object
class heap(object):         # Heap class
    
    def __init__(self, A):
        # Initializing with an array automatically builds the heap
        
        self.heap = A               # Array representation of the heap
        self.heap_size = len(self.heap)-1   # Index where the heap ends. Default is the last element
        
        for j in range(math.floor(len(self.heap)/2)-1, -1, -1):
#            print(j)
            self.max_heapify(j)
        
        
    def max_heapify(self, j):
#        print(j)
        l = self.left(j)
        r = self.right(j)
#        print(j)
        largest = j
        
        if l <= self.heap_size and self.heap[l] > self.heap[j]:
            largest = l
            
        if r <= self.heap_size and self.heap[r] > self.heap[largest]:
            largest = r
            
        if largest != j:
            tmp = self.heap[largest]
            self.heap[largest] = self.heap[j]
            self.heap[j] = tmp
            
            self.max_heapify(largest)
        
#        print(j)
#        print(self.heap)

            
    def left(self, j):
        # Returns the index of the left child node
        return (j << 1) + 1
    
    def right(self, j):
        # Returns the index of the right child node
        return (j << 1) + 2
    
    def draw_heap(self, spacing=2, width=2):
        # Draws the heap        
        
        assert width%2 == 0
        
        # Number of levels = 1 + height of tree
        num_levels = math.floor(math.log(self.heap_size+1,2))+1
        print('heap size '+str(self.heap_size+1))
        print('num levels '+str(num_levels))
        
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
                if 2**height-1+val <= self.heap_size:
                    str_level += fmt.format(self.heap[2**height-1+val])   # Then add the number
                    str_level += ' '*int(spacing_array[height])    # And the space between the numbers
            str_list[height] = str_level

        # Now print
        for height in range(num_levels):
            print(str_list[height]+'\n')
            
        return str_list
        

A = heap([1, 3, 9, 10, 14, 8, 2, 4, 16, 7, 36, 7, 8, 99, 12, 5, 43, 1, 1, 56, 5, 23, 67, 8, 9, 4, 65, 6, 22])

# Check that the left and right functions work as expected
assert(A.left(2)==5)
assert(A.right(1)==4)
assert(A.left(3)==7)

# Check that the heap property is maintained for all nodes
for j in range(A.heap_size+1):
    l = A.left(j)
    r = A.right(j)
    
    if l <= A.heap_size:
        assert A.heap[A.left(j)] <= A.heap[j]
    if r <= A.heap_size:
        assert A.heap[A.right(j)] <= A.heap[j]

str_list = A.draw_heap()



# Heapsort algorithm
def heapsort(array):
    
    # Build the heap
    H = heap(array)
    
    # Take out the first element and reduce the size of the heap
    for j in range(len(array)):
        # Swap the largest element in the heap with the last element in the heap
        tmp = H.heap[0]
        H.heap[0] = H.heap[H.heap_size]   
        H.heap[H.heap_size] = tmp
        
        # Decrement heap size
        H.heap_size -= 1
        
        # Max-Heapify
        H.max_heapify(0)
        
    return H.heap

array = [5, 2, 4, 6, 1, 3]
#print(heapsort(array))
assert heapsort(array) == [1, 2, 3, 4, 5, 6]
array = [31, 41, 59, 26, 41, 58]
#print(heapsort(array))
assert heapsort(array) == [26, 31, 41, 41, 58, 59]


# Quicksort - Chapter 7 CLRS

# First define the partioning function
def partition(A, p=0, r=None):
    # Partition the array A[p:r] for use with Quicksort    
    if r == None:
        r = len(A)-1

    i = p - 1    
    for j_iter in range(r-p):
        j = j_iter + p
#        print(j)
#        print(A)
        
        if A[j] < A[r]:
            i = i + 1
            tmp = A[i]
            A[i] = A[j]
            A[j] = tmp
    
    tmp = A[i+1]
    A[i+1] = A[r]
    A[r] = tmp
    
    return i + 1

array = [5, 2, 4, 6, 1, 3]
partition(array)
assert array == [2, 1, 3, 6, 5, 4]

array = [2, 8, 7, 1, 3, 5, 6, 4]
partition(array)
assert array == [2, 1, 3, 4, 7, 5, 6, 8]

# Quicksort
def quicksort(A, p=0, r=None):
    if r == None:
        r = len(A)-1
    
#    print(p, r)
#    print(A)
    
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q+1, r)
    
    return A

array = [5, 2, 4, 6, 1, 3]
#print(quicksort(array))
assert quicksort(array) == [1, 2, 3, 4, 5, 6]

array = [31, 41, 59, 26, 41, 58]
#print(quicksort(array))
assert quicksort(array) == [26, 31, 41, 41, 58, 59]


# Randomized partition
def partition_random(A, p=0, r=None):
    if r == None:
        r = len(A)-1
        
    rand_idx = random.randint(p, r)
    tmp = A[rand_idx]
    A[rand_idx] = A[r]
    A[r] = tmp
    
    return partition(A, p, r)

array = [5, 2, 4, 6, 1, 3]
partition_random(array)
print(array)

def quicksort_random(A, p=0, r=None):
    if r == None:
        r = len(A)-1
        
    if p < r:
        q = partition_random(A, p, r)
        quicksort_random(A, p, q-1)
        quicksort_random(A, q+1, r)
        
    return A

array = [5, 2, 4, 6, 1, 3]
#print(quicksort(array))
assert quicksort_random(array) == [1, 2, 3, 4, 5, 6]

array = [31, 41, 59, 26, 41, 58]
#print(quicksort(array))
assert quicksort_random(array) == [26, 31, 41, 41, 58, 59]


# Given array A of size n which contains integers from p to p+n, sort A in place
def consecutive_numbers_sort_in_place(A, p=0):
    j = 0
    for j in range(len(A)):
        while A[j] != p+j:
            pos = A[j] - p
            
            tmp = A[pos]
            A[pos] = A[j]
            A[j] = tmp
    return A
            
A = [1, 2, 4, 0, 5, 7, 6, 8, 10, 9, 3]
assert consecutive_numbers_sort_in_place(A) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Counting sort - Pg 195
def counting_sort(A, max_elem=None):
    if max_elem == None:
        max_elem = max(A)
    
    # Initialize the output and count arrays
    out = [0]*len(A)
    count = [0]*(max_elem+1) # Including zeros
    
    # Populate the count array
    for val in A:
        count[val] += 1
#    print(count)
        
    # Keep a running sum
    for idx in range(len(count)-1):
        idx = idx + 1
        count[idx] = count[idx] + count[idx-1]
#    print(count)
        
    # Now sort
    for idx in range(len(A)-1,-1,-1):
        out[count[A[idx]]-1] = A[idx]
        count[A[idx]] -= 1
        
    return out
    
array = [0, 4, 5, 1, 5, 2, 3, 4, 2, 0, 0, 3, 1, 2, 4]
assert counting_sort(array) == [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5]

array = [0, 1, 2, 5, 6, 9, 7, 8, 4, 4, 6, 3, 8, 5, 2, 7, 9, 0, 1, 5, 7, 4, 2, 6, 9]
assert counting_sort(array) == [0, 0, 1, 1, 2, 2, 2, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9, 9]

array = [1, 1, 1, 1, 1]
assert counting_sort(array) == [1, 1, 1, 1, 1]

