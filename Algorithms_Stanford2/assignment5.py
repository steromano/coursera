# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 17:58:28 2014

@author: ste
"""

from itertools import combinations
import numpy as np
import pickle

with open("tsp.txt") as f:
    n = int(f.readline())
    points = [np.array(map(float, line.split())) for line in f]

def eucd(x, y):
    return np.sqrt(sum((x - y)**2))
    
dist = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        dist[i, j] = dist[j, i] = eucd(points[i], points[j])


def without(t, el):
    i = t.index(el)
    return t[:i] + t[(i+1):]


subsets = {k+1 :\
          map(lambda x: (0, ) + x, combinations(range(1, n), k)) for k in range(n)}


for l in subsets:
    if l == 1:
        memois = {(0, ): np.concatenate((np.zeros(1), np.repeat(np.Inf, n-1)))}
        continue
    
    print
    print "Length %d, total subsets %d" %(l, len(subsets[l]))
    print
    count = 0
    new = {}
    for s in subsets[l]:
        count += 1
        if count % 10000 == 0:
            print count
        new[s] = np.repeat(np.Inf, n)
        for j in s:
            if j != 0:
                new[s][j] = min([memois[without(s, j)][k] + dist[k, j] for k in s if k != j])
    memois = new

pickle.dump(memois, open("tsp_memois.p", "wb"))

tsps = memois.values()[0]


print min([tsps[i] + dist[i, 0] for i in range(len(tsps))])


## Let's try to make it faster


memois = {"0":0}
for l in range(2, 3):
    for s in map(lambda t: "".join(map(str, (0, ) + t)), combinations(range(1, n), l-1)):
        print s


