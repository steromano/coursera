# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:45:13 2013

@author: ste
"""
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

#-------------------Initialization-----------------------------

#Graph representation (nodes are labeled by integers):
#Vertices -> dictionary {vertex : [adjacent vertices]}
#Edges -> [tuple(sorted([endpoint, endpoint]))]

#Load vetices
def loadvertices(txtfile):
    vertices={}
    with open(txtfile) as inputgraph:
        for line in inputgraph:
            node=map(int, line.split())
            vertices[node[0]]=node[1:]
    return vertices

#Get edges from adjacency list
def getedges(vertices):
    edges=[]
    for vertex, adjacents, in vertices.iteritems():
        newedges=[]
        for adjacent in adjacents:
            if tuple(sorted([vertex, adjacent])) not in edges:
                newedges.append(tuple(sorted([vertex, adjacent])))
        edges+=newedges
    return edges


#-------------------Visualization-----------------------------

def display(vertices, edges):
    print "Vertices:"
    for vertex, adjacents in vertices.iteritems():
        print str(vertex).ljust(20), adjacents
    print "Edges:"
    print edges

def draw(vertices, edges):
    G=nx.Graph()
    for vertex in vertices:
        G.add_node(vertex)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    nx.draw(G)
    plt.show()


#-------------------Breadth First Search-----------------------------

#Returns a dictionary {vertex : layer} where layer is the distance of vertex from start.
def BFS(vertices, edges, start=1):
    layers={}                   #I can actually avoid allocating a new dictionary, but I'm taking the easy route for now
    for vertex in vertices:
        layers[vertex]=-1       #-1 means infinite distance (different connected component).
                                #All vertices are initialized to have layer -1,
                                #then the algorithm updates their layer.
                                #A nonnegative value means the distance from start.
    layers[start]=0
    q=deque([start])
    while len(q)>0:
        v=q.popleft()
        for w in vertices[v]:
            if layers[w]<0:
                layers[w]=layers[v]+1
                q.append(w)
    return layers

#-------------------Metric-----------------------------

def dist(vertices, edges, start, finish):
    layers=BFS(vertices, edges, start)
    return layers[finish]
    
def max_distance_from(vertices, edges, start):
    layers=BFS(vertices, edges, start)
    return sorted(layers.values())[-1]

def diameter(vertices, edges):
    d=0
    for vertex in vertices:
        dd=max_distance_from(vertices, edges, vertex)
        if dd>d:
            d=dd
    return d
            
#-------------------Connected components-----------------------------

def components(vertices, edges):
    checked=[]
    count=0
    for vertex in vertices:
        if vertex not in checked:
            count+=1
            for node, distance in BFS(vertices, edges, vertex).iteritems():
                if distance>=0:
                    checked.append(node)
    return count
        

#-------------------Main-----------------------------

def main():
    vertices = loadvertices("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/KargerMincut.txt")
    edges=getedges(vertices)
#    display(vertices, edges)    
#    draw(vertices, edges)
    print "The diameter of the graph is", diameter(vertices, edges)
    start=int(raw_input("Enter starting point: "))
    finish=int(raw_input("Enter end point: "))
    print "The maximum distance from %d is %d" %(start, max_distance_from(vertices, edges, start))
    print "The distance between %d and %d is %d." %(start, finish, dist(vertices, edges,start, finish))
#    print "The diameter of the graph is", diameter(vertices, edges)
#    print "Connected components:", components(vertices, edges)

if __name__ == "__main__":
    main()