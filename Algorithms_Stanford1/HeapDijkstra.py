# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 10:11:00 2013

@author: ste
"""

from collections import defaultdict
#import random

"""
-------------------------------------------------------Architecture-------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
I will use the following structures:

1) Vertices adjacency map:
                a dictionary {vertex : [(adjacent_vertex, distance), ...], ...}

2) Edges list:
                a list [(tail, head, length), ...]

3) Greedy-score heap:
                a heapified list [(greedy_score, vertex), ...] of not yet explored vertices, compared w.r.t. greedy score

4) Access map to vertices in the heap:
                a dictionary {vertex : index_in_heap, ...} which keeps track of how vertices are moving in the heap

The last structure is used to find in the heap the vertices adjacent of the last extracted vertex, whose greedy score
needs to be updated. I can't think of a better method. I could include index_in_heap in the adjacency map to save some
space, but I think it's conceptually preferable to keep separated the graph representation from the details of the
algorithm implementation.
"""

"""
-------------------------------------------------------Load Graph---------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""

def loadgraph(filename):
    vertices=defaultdict(list)
    edges=[]
    print 'Loading graph..'
    with open(filename) as inputgraph:
        for line in inputgraph:
            node=line.split()
            vertex=int(node[0])
            for adjacent in node[1:]:
                adjacent_list=tuple(map(int, adjacent.split(',')))
                vertices[vertex].append(adjacent_list)
                if adjacent_list[0] not in vertices:        #Here is where I add vertices with no outgoing edges
                    vertices[adjacent_list[0]]
                edges.append((vertex, adjacent_list[0], adjacent_list[1]))
    
    print 'Graph loaded!'
    return vertices, edges
 
 
"""   
-----------------------------------------------------Display Graph--------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""

def display(vertices, edges = []):
    print '\n'
    print '------------------------Vertices------------------------'
    print '--------------------------------------------------------'
    for vertex in sorted(vertices):
        print str(vertex).ljust(20), vertices[vertex]
        print '\n'
        
    if edges:                                               #I hear this is quite pythonic
        print '\n'
        print '--------------------------Edges-------------------------'
        print '--------------------------------------------------------'
        print edges


"""   
--------------------------------------------------------The heap----------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""

def bubble_down(gsheap, heap_index, start):
    #Input:
    #- is a greedy-score list [(greedy_score, vertex), ...]
    #- heap_index is a dictionary {vertex : index of vertex in gsheap}
    #- start is the index of gsheap to bubble down

    if 2*start+2 < len(gsheap):             #There are two children
        minchild=2*start+1 if gsheap[2*start+1]<gsheap[2*start+2] else 2*start+2
        if gsheap[start]>gsheap[minchild]:
            bubblingdown=gsheap[start][1]   #This vertex is going down
            bubblingup=gsheap[minchild][1]  #This one is going up
            gsheap[start], gsheap[minchild] = gsheap[minchild], gsheap[start]
            heap_index[bubblingdown], heap_index[bubblingup] = heap_index[bubblingup], heap_index[bubblingdown]
            bubble_down(gsheap, heap_index, minchild)
    elif 2*start+1 == len(gsheap)-1:        #There is a single child
        child = 2*start+1
        if gsheap[start]>gsheap[child]:
            bubblingdown=gsheap[start][1]   #This vertex is going down
            bubblingup=gsheap[child][1]     #This one is going up
            gsheap[start], gsheap[child] = gsheap[child], gsheap[start]
            heap_index[bubblingdown], heap_index[bubblingup] = heap_index[bubblingup], heap_index[bubblingdown]

def bubble_up(gsheap, heap_index, start):
    #Same as bubble_down, except we bubble up :)
    if start > 0:
        parent = int((start-1)/2)
        if gsheap[parent]>gsheap[start]:
            bubblingup=gsheap[start][1]
            bubblingdown=gsheap[parent][1]
            gsheap[start], gsheap[parent] = gsheap[parent], gsheap[start]
            heap_index[bubblingup], heap_index[bubblingdown] = heap_index[bubblingdown], heap_index[bubblingup]
            bubble_up(gsheap, heap_index, parent)


#I don't actually need this function for the shortest path algorithm but it's good to have for debugging (and in general).
def heapify(gsheap, heap_index):
    start = int((len(gsheap)-2)/2)
    while (start>= 0):
        bubble_down(gsheap, heap_index, start)
        start-=1

def heap_extract(gsheap, heap_index, index = 0):
    #extracts the element in 'index' position of gsheap and returns (greedy_score, vertex). Extracts min by default
    if index == len(gsheap)-1:                              #this case has to be treated separately
        extracting = gsheap.pop()
        del heap_index[extracting[1]]
        return extracting
        
    extracting = gsheap[index]
    del heap_index[extracting[1]]                           #remove the vertex we are extracting from heap_index
    last=gsheap[-1][1]                                      #last vertex of the list
    gsheap[index], gsheap[-1] = gsheap[-1], gsheap[index]   #switch the last and 'index'-th position
    gsheap.pop()                                            #remove last
    heap_index[last]=index                                  #update index of last in heap_index
    
    bubble_up(gsheap, heap_index, index)
    bubble_down(gsheap, heap_index, index)                  #At least one of these two calls does nothing
    
    return extracting

def heap_insert(gsheap, heap_index, element):
    #Input:
    #gsheap and heap_index are as usual
    #element is a tuple (greedy_score, vertex) to be inserted in gsheap. The vertex has also to be inserted in heap_index
    gsheap.append(element)
    heap_index[element[1]]=len(gsheap)-1
    bubble_up(gsheap, heap_index, heap_index[element[1]])



"""   
--------------------------------------------------Dijkstra's shortest path------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""

def update(vertices, distances, gsheap, heap_index, last_extracted):
    #updates the heap (gsheap-heap_index) with the new greedy scores of the vertices adjacent to last_extracted
    #lying outside of the frontier
    for adjacent, distance in vertices[last_extracted]:
        if adjacent not in distances:
            new_greedy = distances[last_extracted]+distance
            if new_greedy < gsheap[heap_index[adjacent]][0]:
                heap_extract(gsheap, heap_index, heap_index[adjacent])
                heap_insert(gsheap, heap_index, (new_greedy, adjacent))

def DijkstraSP(vertices, start):
    #Returns a dictionary {vertex : distance from start}
    
    distances = {start:0}
    
#---Initialize the greedy score heap:
    gsheap=[]
    heap_index={}
    i=0
    for vertex in vertices:                                     #Here I put everything into gsheap, including start,
        gsheap.append((float('inf'), vertex))                   #and initialize all greedy scores to infinity
        heap_index[vertex]=i
        i+=1
    heap_extract(gsheap, heap_index, heap_index[start])         #Remove start from the heap
    update(vertices, distances, gsheap, heap_index, start)      #and update the greedy scores of the neighboors    
    
#---The main while loop
    while len(distances) < len(vertices):
        greedy_score, next_vertex = heap_extract(gsheap, heap_index)
        distances[next_vertex] = greedy_score
        update(vertices, distances, gsheap, heap_index, next_vertex)
    
    return distances
    
    
    
"""   
------------------------------------------------------------Main----------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""
 
def main():
    vertices, edges = loadgraph("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/Dijkstradata.txt")
    #display(vertices)
    start = int(raw_input("Enter starting point: "))
    distances = DijkstraSP(vertices, start)
    for vertex in sorted(distances):
        print ("Vertex: %d" %vertex).ljust(20) +"Distance from %d: %d" %(start, distances[vertex])
        
if __name__ == '__main__':
    main()
