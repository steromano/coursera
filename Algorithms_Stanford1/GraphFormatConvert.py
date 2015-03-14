# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:33:32 2013

@author: ste
"""

#Convert input file for graph from adjacency list version, where each line is
#vertex adjacent adjacent adjacent ...
#to edge representation where each line is
#tail head

edges=[]
with open("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/KargerMinCut.txt") as v_list_file:
    for line in v_list_file:
        node=map(int, line.split())
        for adjacent in node[1:]:
            edges.append([node[0], adjacent])

with open("/Users/ste/Desktop/Ste/C++/Programs/AlgorithmCourse/GraphSearch/KargerMinCut(edges).txt", "w+") as outfile:
    for edge in edges:
        outfile.write(str(edge[0])+' '+str(edge[1])+'\n')
    