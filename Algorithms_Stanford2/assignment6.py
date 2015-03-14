# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 12:40:03 2014

@author: ste

"""


class graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges= edges
        self.g = {v:[] for v in vertices}
        for h, t in edges:
            self.g[h].append(t)
            
    def init_dfs(self):
        self.flags = {v:{"explored": None, "source": None} for v in self.vertices}        
        self.dfs_finish_order = []

            
    def reverse(self):
        reverse_edges = [(t, h) for h, t in self.edges]
        self.__init__(self.vertices, reverse_edges)
        
    def dfs(self, start):
        stack = [start]
        self.flags[start] = {"explored": True, "source": start}
        while len(stack) > 0:
            last = stack[-1]
            count_newv = 0
            for v in self.g[last]:
                if not self.flags[v]["explored"]:
                    self.flags[v] = {"explored": True, "source": start}
                    stack.append(v)
                    count_newv +=1
            if count_newv == 0:
                self.dfs_finish_order.append(stack.pop())
                
    def dfs_loop(self, order = None):
        if order is None:
            order = self.vertices
        
        self.init_dfs()
        
        for start in order:
            if not self.flags[start]["explored"]:
                self.dfs(start)
    
    def scc(self):
        self.reverse()
        self.dfs_loop()
        self.reverse()
        self.dfs_finish_order.reverse()
        self.dfs_loop(order = self.dfs_finish_order)
        
        sccs = {}
        for v, flag in self.flags.iteritems():
            sccs[flag["source"]] = sccs.get(flag["source"], []) + [v]
        
        return sccs
        
        
    
    
    

class twosat:
    def __init__(self, infile):
        with open(infile) as f:
            self.n = int(f.readline())
            self.clauses = [map(int, line.split()) for line in f]
            self.make_graph()
    
    def make_graph(self):
        vertices = [k for k in range(-self.n, self.n+1) if k!= 0]
        edges = []
        for a, b in self.clauses:
            edges.append((-a, b))
            edges.append((-b, a))
        self.graph = graph(vertices, edges)
    
    def has_solution(self):
        self.scc = self.graph.scc()
        for s, c in self.scc.iteritems():
            if len(set(map(abs, c))) != len(c):
                return False
        return True

solution = []
for i in range(1, 7):
    print i
    ts = twosat("2sat" + str(i) + ".txt")
    solution.append(int(ts.has_solution()))

print int("".join(map(str, solution)))
   

