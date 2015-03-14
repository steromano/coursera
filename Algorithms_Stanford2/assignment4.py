# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 11:12:25 2014

@author: ste
"""

import numpy as np

class graph:
    def __init__(self, infile = None):
        if infile is not None:
            with open(infile) as f:
                self.n, self.m = map(int, f.readline().split())
                self.edges = [tuple(map(int, line.split())) for line in f]
    
    def set_graph(self, edges):
        self.edges = edges
        self.n, self.m = len(set([v for (v, _, _) in edges] + [u for (_, u, _) in edges])), len(edges)
    
    def set_pointers(self):
        self.heads, self.tails = {}, {}
        for (h, t, l) in self.edges:
            self.heads[h] = self.heads.get(h, []) + [(t, l)]
            self.tails[t] = self.tails.get(t, []) + [(h, l)]
            
    def __repr__(self):
        dots = "..." if self.m > 10 else ""
        return ("n, m = %d, %d\n\n" %(self.n, self.m) + \
                '\n'.join(map(str, self.edges[:min(self.m, 10)]) + [dots])) 

# test case
edges = [(1, 2, 3),
         (2, 4, 0),
         (1, 5, -4),
         (5, 4, 2),
         (3, 5, -3),
         (6, 3, -2),
         (6, 5, 6),
         (4, 6, 5)]

g = graph()
g.set_graph(edges)


def floyd_warshall(g):
    A = np.zeros((g.n+1, g.n, g.n))
    A[0, :, :].fill(np.Inf)
    for i in range(g.n):
        A[0, i, i] = 0
    for (h, t, l) in g.edges:
        A[0, h-1, t-1] = l
    for k in range(1, g.n+1):
        print k
        for i in range(1, g.n+1):
            for j in range(1, g.n+1):
                A[k, i-1, j-1] = min(A[k-1, i-1, j-1], A[k-1, i-1, k-1]+A[k-1, k-1, j-1])
        if np.diag(A[k, :, :]).sum() < 0:
            print "Negative cycle detected"
            return None
 
    return A[g.n-1, :, :]    

g1 = graph("g1.txt")
A1 = floyd_warshall(g1)  # negative cycle found

g2 = graph("g2.txt")
A2 = floyd_warshall(g2)  # negative cycle found

g3 = graph("g3.txt")
A3 = floyd_warshall(g3)
print A3.min()


def bellmann_ford(g, s):
    if 'tails' not in dir(d):
        g.set_pointers()
    A = np.zeros((g.n+1, g.n))
    A[0, :].fill(np.Inf)
    A[0, s-1] = 0
    for k in range(1, g.n+1):
        for v in range(1, g.n+1):
            A[k, v-1] = min([A[k-1, v-1]] + \
                          [A[k-1, w-1] + l for (w, l) in g.tails.get(v, [])])
            if k < g.n and np.array_equal(A[k-1, :], A[k, :]):
                return A[k, :]
    if not np.array_equal(A[g.n-1, :], A[g.n, :]):
        print "Negative cycle detected"
        return None
    return A[g.n, :]
        
def n_bellmann_ford(g):
    g.set_pointers()
    A = np.zeros((g.n, g.n))
    for s in g.heads:
        print s
        from_s = bellmann_ford(g, s)
        if from_s is not None:
            A[s-1, :] = from_s
        else:
            return None  
    return A    
           
    
    

    