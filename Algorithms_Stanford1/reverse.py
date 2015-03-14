# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:42:59 2013

@author: ste
"""

#This script takes a text file representing a graph with the same conventions of SCC.txt (1 line per edge, sorted by the tail
#vertex) and creates an identical representation for the grah with all edges reversed.
#If the input file is 'filename', the output is stored in 'filename.reversed'.

import sys

filename = sys.argv[1]
edges=[]

with open(filename) as inputgraph:
    for line in inputgraph:
        edge = map(int, line.split())
        edges.append([edge[1], edge[0]])

with open(filename+'.reversed', 'w+') as output:
    for line in sorted(edges):
        output.write(str(line[0])+' '+str(line[1])+'\n')