# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:31:13 2014

@author: ste
"""

import os
import numpy as np
os.chdir('Desktop/Ste/Python/AlgorithmsCourse2')

infile = 'knapsack1.txt'
with open(infile) as f:
    c, n = map(int, f.readline().split())
    items = [(value, weight) for (value, weight) in map(lambda row: map(int, row.split()), f)]
    
#c, n = 6, 4  
#items = [(5, 3), (2, 1), (4, 5), (8, 6)]
    
#c, n = 6, 4
#items = [(3, 4), (2, 3), (4, 2), (4, 3)]
  
memois = np.zeros((c+1, n+1))

for j in range(1, n+1):
    print j
    for i in range(1, c+1):
        v, w = items[j-1]
        if i >= w:
            memois[i, j] = max(memois[i, j-1], memois[i-w, j-1] + v)
        else:
            memois[i, j] = memois[i, j-1]

print memois[c, n]


old = np.zeros(c+1)
new = np.zeros(c+1)
counter = 0

for (v, w) in items:
    print counter
    new[:w] = old[:w]
    for i in range(w, len(old)):
        new[i] = max(old[i], old[i-w] + v)
    old[:] = new[:]
    counter += 1
        
print new[-1]


c = np.diag((5, 40, 8, 4, 10, 10, 23))

for i in range(6):
    c[i, i+1] = c[i, i] + c[i+1, i+1] + min(c[i, i], c[i+1, i+1])

for i in range(5):
    c[i, i+2] = sum([c[j, j] for j in range(i, i+3)]) + \
                min([c[i, i+1]] + [c[i, j] + c[j+2, i+2] for j in range(i, i+1)] + [c[i+1, i+2]])
for i in range(4):
    c[i, i+3] = sum([c[j, j] for j in range(i, i+4)]) + \
                min([c[i, i+2]] + [c[i, j] + c[j+2, i+3] for j in range(i, i+2)] + [c[i+1, i+3]])

for i in range(3):
    c[i, i+4] = sum([c[j, j] for j in range(i, i+5)]) + \
                min([c[i, i+3]] + [c[i, j] + c[j+2, i+4] for j in range(i, i+3)] + [c[i+1, i+4]])

for i in range(2):
    c[i, i+5] = sum([c[j, j] for j in range(i, i+6)]) + \
                min([c[i, i+4]] + [c[i, j] + c[j+2, i+5] for j in range(i, i+4)] + [c[i+1, i+5]])

for i in range(1):
    c[i, i+6] = sum([c[j, j] for j in range(i, i+7)]) + \
                min([c[i, i+5]] + [c[i, j] + c[j+2, i+6] for j in range(i, i+5)] + [c[i+1, i+6]])