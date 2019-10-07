# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:09:55 2019

@author: Sai
"""
import time

# Rod cutting problem - Chap 15.1 of CLRS
rod_length =  [0, 1, 2, 3, 4,  5,  6,  7,  8,  9, 10]
price_array = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]

# Recursive solution Pg 363
def cut_rod_recursive(price, length):
    if length == 0:
        return 0
    q = -1
    for idx in range(1,length+1):
        q = max(q, price[idx]+cut_rod_recursive(price, length-idx))
    return q

# Test cases from Pg 362
assert cut_rod_recursive(price_array, 7) == 18
assert cut_rod_recursive(price_array, 9) == 25
assert cut_rod_recursive(price_array, 10) == 30

# Print some runtimes for arbitrary price array
t = time.time()
cut_rod_recursive([2]*51, 10)
print('Recursive version run time for length = 10: '+str(time.time()-t))
t = time.time()
cut_rod_recursive([2]*51, 15)
print('Recursive version run time for length = 15: '+str(time.time()-t))
t = time.time()
cut_rod_recursive([2]*51, 20)
print('Recursive version run time for length = 20: '+str(time.time()-t))
#t = time.time()
#cut_rod_recursive([2]*51, 23)
#print('Recursive version run time for length = 23: '+str(time.time()-t))


# Top-down memoized solution Pg 365
def cut_rod_memoized(price, length):
    optimal_price = [-1]*(length+1)
    optimal_price[0] = 0
    return cut_rod_memoized_aux(price, length, optimal_price)
    
def cut_rod_memoized_aux(price, length, optimal_price):
    if optimal_price[length] == -1:
        # Calculate recursively
        q = -1
        for idx in range(1, length+1):
            q = max(q, price[idx]+cut_rod_memoized_aux(price, length-idx, optimal_price))
        optimal_price[length] = q
        return q
    else:
        # Lookup in the array
        return optimal_price[length]
    
# Test cases from Pg 362
assert cut_rod_memoized(price_array, 7) == 18
assert cut_rod_memoized(price_array, 9) == 25
assert cut_rod_memoized(price_array, 10) == 30

# Print some runtimes for arbitrary price array
t = time.time()
cut_rod_memoized([2]*51, 10)
print('Memoized version run time for length = 10: '+str(time.time()-t))
t = time.time()
cut_rod_memoized([2]*51, 15)
print('Memoized version run time for length = 15: '+str(time.time()-t))
t = time.time()
cut_rod_memoized([2]*51, 20)
print('Memoized version run time for length = 20: '+str(time.time()-t))
t = time.time()
cut_rod_memoized([2]*101, 100)
print('Memoized version run time for length = 100: '+str(time.time()-t))


# Bottom-up version Pg 366
def cut_rod_bottom_up(price, length):
    optimal_price = [-1]*(length+1)
    optimal_price[0] = 0
    
    for i in range(1, length+1):
        q = -1
        for j in range(1, i+1):
            q = max(q, price[j]+optimal_price[i-j])
        optimal_price[i] = q
    
    return optimal_price[length]

# Test cases from Pg 362
assert cut_rod_bottom_up(price_array, 7) == 18
assert cut_rod_bottom_up(price_array, 9) == 25
assert cut_rod_bottom_up(price_array, 10) == 30

# Print some runtimes for arbitrary price array
t = time.time()
cut_rod_bottom_up([2]*51, 10)
print('Bottom up version run time for length = 10: '+str(time.time()-t))
t = time.time()
cut_rod_bottom_up([2]*51, 15)
print('Bottom up version run time for length = 15: '+str(time.time()-t))
t = time.time()
cut_rod_bottom_up([2]*51, 20)
print('Bottom up version run time for length = 20: '+str(time.time()-t))
t = time.time()
cut_rod_bottom_up([2]*101, 100)
print('Bottom up version run time for length = 100: '+str(time.time()-t))

# Bottom up cut-rod with printing of the cuts
def cut_rod_bottom_up_print(price, length):
    optimal_price = [-1]*(length+1)
    optimal_price[0] = 0
    cuts = [0]*(length+1)
    
    for i in range(1, length+1):
        q = -1
        for j in range(1, i+1):
            if price[j]+optimal_price[i-j] > q:
                q = price[j]+optimal_price[i-j]
                cuts[i] = j
                
        optimal_price[i] = q

    cut_length = length
    while cut_length > 0:
        print(cuts[cut_length])
        cut_length = cut_length - cuts[cut_length]
        
    return optimal_price[length]

# Test cases from Pg 362
assert cut_rod_bottom_up_print(price_array, 7) == 18
assert cut_rod_bottom_up_print(price_array, 9) == 25
assert cut_rod_bottom_up_print(price_array, 10) == 30


# Longest common subsequence - Pg 394-395
def lcs(seq1, seq2):
    # Array to store the length of the LCS of the substrings seen so far
    length = [[0]*(len(seq2)+1) for i in range(len(seq1)+1)]
    
    # Array to store the steps taken. Used to reconstruct the LCS. The values mean the following:
    # 1 - drop the last character in seq1
    # 2 - drop the last character in seq2
    # 3 - last characters are the same, so the character is added to the LCS
    step = [[0]*(len(seq2)+1) for i in range(len(seq1)+1)]
    
    for i1, c1 in enumerate(seq1, 1):
        for i2, c2 in enumerate(seq2, 1):
#            print(i1, i2, c1, c2)
            if c1 == c2:
                length[i1][i2] = length[i1-1][i2-1] + 1
                step[i1][i2] = 3
#                print(3)
            elif length[i1-1][i2] > length[i1][i2-1]:
                length[i1][i2] = length[i1-1][i2]
                step[i1][i2] = 1
#                print(1)
            else:
                length[i1][i2] = length[i1][i2-1]
                step[i1][i2] = 2
#                print(2)
#            print(length)
#    print(length)
#    print(step)
                
    p1 = len(seq1)
    p2 = len(seq2)
    LCS = ''
    while p1 > 0 and p2 > 0:
        if step[p1][p2] == 1:
            p1 -= 1
        elif step[p1][p2] == 2:
            p2 -= 1
        elif step[p1][p2] == 3:
#            print(p1, p2, seq1[p1-1], seq2[p2-1])
            LCS += seq1[p1-1]
            p1 -= 1
            p2 -= 1
           
    return LCS[::-1]

seq1 = 'TCG'
seq2 = 'TAC'
#print(lcs(seq1, seq2))
assert lcs(seq1, seq2) == 'TC'

seq1 = 'TGACTGGGT'
seq2 = 'GGGG'
#print(lcs(seq1, seq2))
assert lcs(seq1, seq2) == 'GGGG'

# Test case from Pg 391 of CLRS
seq1 = 'ACCGGTCGAGTGCGCGGAAGCCGGCCGAA'
seq2 = 'GTCGTTCGGAATGCCGTTGCTCTGTAAA'
#print(lcs(seq1, seq2))
assert lcs(seq1, seq2) == 'GTCGTCGGAAGCCGGCCGAA'