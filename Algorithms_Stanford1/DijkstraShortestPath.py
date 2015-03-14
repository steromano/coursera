# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 22:31:21 2013

@author: ste
"""

from collections import defaultdict

#--------------------------------------------------Graph Representation---------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
"""
Vertices:   dictionary {vertex:[[adjacent_vertex, distance], ...], ...}
Edges:      list [(tail, head, length), ...]
"""

#------------------------------------------------------Load Graph---------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

def loadgraph():
    vertices=defaultdict(list)
    edges=[]
    print 'Loading graph..'
    with open("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/Dijkstradata.txt") as inputgraph:
        for line in inputgraph:
            node=line.split()
            vertex=int(node[0])
            for adjacent in node[1:]:
                adjacent_list=map(int, adjacent.split(','))
                vertices[vertex].append(adjacent_list)
                if adjacent_list[0] not in vertices:        #Here is where I add vertices with no outgoing edges
                    vertices[adjacent_list[0]]
                edges.append((vertex, adjacent_list[0], adjacent_list[1]))
    
    print 'Graph loaded!'
    return vertices, edges

#----------------------------------------------------Display Graph--------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

def display(vertices, edges):
    print '\n'
    print '------------------------Vertices------------------------'
    print '--------------------------------------------------------'
    for vertex in sorted(vertices):
        print str(vertex).ljust(20), vertices[vertex]

    print '\n'
    print '--------------------------Edges-------------------------'
    print '--------------------------------------------------------'
    print edges

#------------------------------------------------Dijstra Shortest Path----------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

def DijkstraSP(start, vertices, edges):
    distances = {start:0}
    n=len(vertices)
    while len(distances)<n:                    
        next_vertex=(-1, float('inf'))                  #This is a pair (candidate vertex, greedy score)
        for edge in edges:
            if edge[0] in distances and edge[1] not in distances:
                greedy_score=distances[edge[0]]+edge[2]
                if greedy_score<next_vertex[1]:
                    next_vertex = (edge[1], greedy_score)
        distances[next_vertex[0]]=next_vertex[1]
    return distances
    
#---------------------------------------------------------Main------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
    
def main():
    vertices, edges = loadgraph()    
    #display(vertices, edges)    
    #start = int(raw_input("Enter starting point: "))
    start=1
    distances = DijkstraSP(start, vertices, edges)
    for vertex in sorted(distances):
        astring = "Vertex: %d" %vertex
        print astring.ljust(20)+"Distance from %d: %d" %(start, distances[vertex])




if __name__ == '__main__':
    main()