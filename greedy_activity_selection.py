# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:01:15 2019

@author: Sai
"""

# Activity selection problem - maximize the number of activities given a list
# of activities that are sorted by their finish times
# Pg 421 CLRS

def activity_selection(s, f):
    list_activities = [0]   # Always take the first activity
    m = 0                   # Index of the activity last added
    
    for k in range(1, len(f)):
        if s[k] >= f[m]:    # Activity can be added
            list_activities.append(k)
            m = k           # Update index
            
    return list_activities

# Test case from Pg 415
s = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]
f = [4, 5, 6, 7, 9, 9, 10, 11, 12, 14, 16]
assert activity_selection(s, f) == [0, 3, 7, 10]