# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:05:12 2013

@author: ste
"""

import random
import copy

#----------------------------------------------------------
#Utility stuff
#----------------------------------------------------------

#Display vertices and edges           
def display(vertices, edges):
    print "Vertices:"
    for vertex, adjacents in vertices.iteritems():
        print str(vertex).ljust(20), adjacents
    print "Edges:"
    print edges

#Convert integers to sigle-element tuples (also works for lists of integers and dictionaries with integer keys and values)
#This is just for convenience in the initial loading of the graph, since I chose to represent each vertex (including singles) by a tuple.
def int_to_tuple(x):
    if type(x)==int:
        return tuple([x])
    elif type(x)==list:
        return [int_to_tuple(el) for el in x]
    elif type(x)==dict:
        converted={}
        for key in x:
            converted[int_to_tuple(key)]=int_to_tuple(x[key])
        return converted

#Flattens a tuple of tuples into a single tuple
def flatten(nestedtuples):
    return tuple([el for atuple in nestedtuples for el in atuple])
    
#---------------------------------------------------------
#---------------------------------------------------------


#Computes the list of edges from the dictionary of vertices ({vertex:adjacent vertices})
def getedges(vertices):
    edges=[]
    for vertex, adjacents, in vertices.iteritems():
        newedges=[]
        for adjacent in adjacents:
            if sorted([vertex, adjacent]) not in edges:
                newedges.append(sorted([vertex, adjacent]))
        edges+=newedges
    return edges

#----------------------------------------------------------
#The main function.
#Contracts the kth vertex, deletes self-liks and updates the list of edges
def contract(vertices, edges, k):
    contracted=edges.pop(k)
    
#---Add new contraced vertex
    newvertex=flatten(tuple(contracted))
    vertices[newvertex]=vertices[contracted[0]]+vertices[contracted[1]]
    
#---Replace all instances of all vertices with the new contracted vertex. I can do it by looping only on neightbours of the 
    #new vertex (first version, commented), but quit incredibly looping over all vertices is quite a bit faster (?!?).

#    for next_to_new in vertices[newvertex]+[newvertex]:
#        adjacents=vertices[next_to_new]
#        for i in range(len(adjacents)):
#            if adjacents[i]==contracted[0] or adjacents[i]==contracted[1]:
#                adjacents[i]=newvertex
    
    for vertex, adjacents in vertices.iteritems():
        for i in range(len(adjacents)):
            if adjacents[i]==contracted[0] or adjacents[i]==contracted[1]:
                adjacents[i]=newvertex

#---Delete the two old vertices
    del vertices[contracted[0]]
    del vertices[contracted[1]]

#---Erase self loops from contracted vertex
    #I use a list comprehension fo remove all elements in the list (of adjacent elements to newvertex) equal to the newvertex.
    #Note the use of [:] to make sure the list is modified in place.
    vertices[newvertex][:]=[adjacent for adjacent in vertices[newvertex] if adjacent != newvertex]    
    
#---Update edges. Two versions: the second one (commented) uses two consecutive loops over edges: the first replaces the
    #instances of the old vertices with the new one, and the second erases self-loops. The first version (which I'm using)
    #does both with a single loop, removing self-loops while looping (which is supposedly faster). To achieve this, 
    #the trick is to loop backwards (!).
    for j in range(len(edges)-1, -1, -1):
        for i in range(2):
            if edges[j][i]==contracted[0] or edges[j][i]==contracted[1]:
                edges[j][i]=newvertex
        if edges[j][0]==edges[j][1]:
            edges.pop(j)
#    for edge in edges:
#        for i in range(2):
#            if edge[i]==contracted[0] or edge[i]==contracted[1]:
#                edge[i]=newvertex
#    edges[:]=[edge for edge in edges if edge[0]!=edge[1]]   #Delete selfedges     
    #edges[:]=getedges(vertices)            SLOW!!
    
#---Seems to make sense to return the contracted edge, not sure why.
    return contracted
#-----------------------------------------------------------

          
#Test    
#loaded={1:[2, 3, 4], 2:[1, 6, 7], 3:[1, 4, 7, 6, 5], 4:[1, 3, 7], 5:[3, 6, 6], 6:[5, 5, 3, 2], 7:[3, 4, 2]}

#Load the true graph

loaded={}
with open("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/kargermincut.txt") as inputgraph:
    for line in inputgraph:
        node=map(int, line.split())
        loaded[node[0]]=node[1:]

loaded=int_to_tuple(loaded)
loaded_edges=getedges(loaded)
mincut_length, mincut = len(loaded.keys()), []

print "Graph loaded!"

def generate():
    global loaded, loaded_edges, mincut_length, mincut         
    vertices=copy.deepcopy(loaded)  #Really need to make a deep copy here to avoid troubles (the values contained in the dictionary are modified in place when calling contract).
    edges=copy.deepcopy(loaded_edges)
    while(len(vertices)>2):
        contract(vertices, edges, random.randrange(len(edges)))
    if len(edges)<mincut_length:
        mincut_length=len(edges)
        mincut=map(sorted, vertices.keys())
    print "Random cut generated. Lenght =", len(edges), "\tThe minimum lenght so far is", mincut_length

    

samplesize=200
for i in range(samplesize):            
    generate()
    
print "%d random cuts generated. The minimum lenght achieved was %d" %(samplesize, mincut_length)
print "The corresponding cut is"
print mincut[0]
print "Structure: (%d, %d)" %(len(mincut[0]), len(mincut[1]))


    