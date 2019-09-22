# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 12:42:29 2019

@author: Sai
"""
import math


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
            self.max_heapify(j)
        
        
    def max_heapify(self, j):
        l = self.left(j)
        r = self.right(j)
        
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
    
#    def draw_heap(self):
#        # Draws the heap
#        num_levels = math.floor(math.log(A.heap_size))
#        
#        for j in range(num_levels):
#            num_nodes = A.heap_size/(2**(j+1))
#            start_space = '\t'*(j/2)
#            


A = heap([1, 3, 9, 10, 14, 8, 2, 4, 16, 7, 36, 7, 8, 99, 12, 5, 43, 1])

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
    
    q = partition(A, p, r)
    if q-p > 1:
        quicksort(A, p, max(0, q-1))
    if r-q > 1:
        quicksort(A, min(q+1, len(A)-1), r)
    
#    print(p, q, r)
    return A

array = [5, 2, 4, 6, 1, 3]
#print(quicksort(array))
assert quicksort(array) == [1, 2, 3, 4, 5, 6]

array = [31, 41, 59, 26, 41, 58]
#print(quicksort(array))
assert quicksort(array) == [26, 31, 41, 41, 58, 59]