# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 20:34:34 2014

@author: ste
"""

class heap:
    def __init__(self, l = None):
        self.tree = []
        if l != None:
            for x in l:
                self.insert(x)
    def __len__(self):
        return len(self.tree)
    def __repr__(self):
        s = ""
        for i in range(len(self)):
            c = self.children(i)
            if len(c) > 0:
                s += "Parent node: %d\n" %self.tree[i]
                s += "Children nodes:" + str(map(lambda j: self.tree[j], c)) + "\n"
        return s
    def has_heap_property(self):
        for i in range(len(self)):
            c = self.children(i)
            if len(c) > 0 and min([self.tree[i]] + map(lambda j: self.tree[j], c)) != self.tree[i]:
                return False
        return True
    def parent(self, i):
        j = (i-1)/2
        if j >= 0 and j < len(self):
            return j
        else:
            return None
    def children(self, i):
        return [j for j in (2*i+1, 2*i+2) if j < len(self)]
    def switch(self, i, j):
        self.tree[i], self.tree[j] = self.tree[j], self.tree[i]
    def bubble_up(self, i):
        while i > 0 and self.tree[self.parent(i)] > self.tree[i]:
            self.switch(i, self.parent(i))
            i = self.parent(i)
    def bubble_down(self, i):
        c = self.children(i)
        while len(c) > 0:
            m = min(c, key = lambda k: self.tree[k])
            if self.tree[m] >= self.tree[i]:
                break
            else:
                self.switch(i, m)
                i = m
                c = self.children(i)
    def insert(self, x):
        self.tree.append(x)
        self.bubble_up(len(self) - 1)
    def extract_min(self):
        self.switch(0, len(self) - 1)
        minimum = self.tree.pop()
        self.bubble_down(0)
        return minimum
    def delete(self, i):
        self.switch(i, len(self) - 1)
        self.tree = self.tree[:-1]
        self.bubble_down(i)
       
def heapsort(l):
    h = heap(l)
    return [h.extract_min() for _ in range(len(l))]
        
        