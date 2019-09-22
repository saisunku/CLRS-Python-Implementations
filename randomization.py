# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 19:50:51 2019

@author: Sai
"""

import random


def random01():
    # Function that returns 0 with probability 1/2 and 1 with probability 1/2
    return random.randrange(2)

print(random01())
print(random01())

def randomab(a, b):
    # Function that returns an integer between a and b with equal probability
    # Solution to Problem 5.1-2 in CLRS
    
    assert a < b
    
    minimum = a
    maximum = b
    
    while abs(maximum - minimum) > 0.5:
        if random01() == 0:
            minimum = (minimum+maximum)/2
        else:
            maximum = (minimum+maximum)/2
            
    return int(minimum)
        
print(randomab(2, 10))
print(randomab(2, 10))
print(randomab(2, 10))
print(randomab(2, 10))

# Randomize-In-Place algorithm from Pg 126
def randomize_in_place(A):
    for j in range(len(A)):
        random_idx = randomab(j, len(A))
        tmp = A[j]
        A[j] = A[random_idx]
        A[random_idx] = tmp
        
    return A

A = [1, 5, 7, 6 ,2, 4, 8, 4, 8, 6]
print(randomize_in_place(A))
print(randomize_in_place(A))
print(randomize_in_place(A))
