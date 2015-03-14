# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 18:54:19 2014

@author: ste
"""

with open("jobs.txt") as f:
    njobs = int(f.readline())
    jobs = [(weight, length) for (weight, length) in map(lambda line : map(int, line.split()), f)]

def wsum(jobs):
    cumsum = 0
    finals = []
    for weight, length in jobs:
        cumsum += length
        finals.append((weight, cumsum))
    return sum(map(lambda (weight, final_time): weight * final_time, finals))

scheduled1 = sorted(jobs, key = lambda (weight, length) : [- (weight - length), - weight])
scheduled2 = sorted(jobs, key = lambda (weight, length) : [- float(weight) / length, - weight])
print wsum(jobs)
print wsum(scheduled1)
print wsum(scheduled2)

with open("edges.txt") as f:
    n, m = map(int, f.readline().split())
    graph = [(node1, node2, cost) for (node1, node2, cost) in 
             map(lambda line: map(int, line.split()), f)]



def crossing(conquered, graph):
    return [(n1, n2, cost) for (n1, n2, cost) in graph if (n1 in conquered) != (n2 in conquered)]

conquered = [graph[43][0]]
mst = []

while len(conquered) < n:
    print len(conquered)
    frontier = crossing(conquered, graph)
    new_edge = min(frontier, key = lambda (n1, n2, cost): cost)
    mst.append(new_edge)
    if new_edge[0] in conquered:
        conquered.append(new_edge[1])
    else:
        conquered.append(new_edge[0])

print sum(map(lambda (n1, n2, cost): cost, mst))