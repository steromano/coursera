# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:42:50 2013

@author: ste
"""


#---------------------------------------------------Graph loading------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

#Input format is a text file containing a pair of integers per line, representing a directed edge (from first integer 
#-tail- to second integer -head-). The list is sorted by the tail vertex.

#WARNING!!
#For convenience I'm relabeling all the vertices to go from 0 to n-1 instead of from 1 to n.
#This makes it easier to idenfify vertex labels with list indexes, which start from zero in Python.
#Therefore in the representation of the graph inside the script the labels of the vertices are shifted by 1
#w.r.t. the input.

#Graph representation:
#Vertices -> list where the i-th element is a list of the vertices to which the i-th vertex points.
#Edges -> I don't need edges!

#This takes the input file in theabove format and returns the vertices list in the above representation. This function
#is quite horrible and should probably be rewritten. It is possibly a better idea to accept using a little more memory
#and store vertices in a dictionary instead of a list.
def loadgraph(filename):
    print 'Loading graph...'
    with open(filename) as inputgraph:        
        vertices=[]
        max_vertex=-1
        for line in inputgraph:
                    #Here I read the data into a list of integers and shift them by 1.
            edge=map(lambda x: int(x)-1, line.split())
            if edge[1]>max_vertex:
                max_vertex=edge[1]
            if edge[0]==len(vertices)-1:
                vertices[edge[0]].append(edge[1])
            elif edge[0]>=len(vertices):
                    #Some vertices have no outgoing edges. Here I assign the empty list to them. This works for
                    #vertices in the middle of the list but FAIL for vertices at the end of the list. See below.
                for i in range(len(vertices), edge[0]):
                    vertices.append([])
                vertices.append([edge[1]])
        k=len(vertices)
        for i in range(k, max_vertex+1):    #I need to to this horrible thing to account for the case where the
            vertices.append([])             #vertices with te highest label have no outgoing vertices, and therefore
                                            #never appear in the list in tail position 
    print 'Graph loaded!'
    return vertices                         
    
#------------------------------------------------------Utility---------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
    
#Use this only for small test graphs.
def display(vertices):
    for i in range(len(vertices)):
        print str(i).ljust(20), vertices[i]
    
 
#-------------------------------------------------Depth First Search---------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

#Global variables
flags=[]         #Global list of book-keeping info about vertices. The i-th entry is a dictionary keeping track
                 #of global flags for the i-th vertex. Keys are: 'explored' and 'source' (got rid of final_time).
source=-1        #Global variable keeping track of the source vertex of each DFScall.
finish_order=[]  #When the first pass is done with a vertex it appends it to finish_order. Then second pass loops
                 #on the vertices in the (reversed) order of this list.
           

#Call this with n=len(vertices) before starting doing stuff with DFS.
#It just sets all vertices to unexplored and resets all source flags.
def initialize_flags(n):
    global flags, source 
    flags, source = [], -1  
    for i in range(n):
        flags.append({'explored': False, 'source':-1})
        
#The recursive version of DFS. This exceeds the recursion depth for the huge graph (~800000 nodes) of the assignment!
def recursive_DFS(vertices, start):
    global flags
    flags[start]['explored']=True
    print 'Exploring', start
    for v in vertices[start]:
        if not flags[v]['explored']:
            recursive_DFS(vertices, v)

#The non recursive version using a stack.
def DFS(vertices, start, second_pass=False):    #I'm adding the boolean here to avoid recording the finish order
    global flags, source                        #on the second pass
    DFSstack=[start]
    while(len(DFSstack)>0):
        last=DFSstack[-1]
        if not flags[last]['explored']:
            flags[last]['explored']=True
            flags[last]['source']=source
        i=0
        while(i<len(vertices[last]) and flags[vertices[last][i]]['explored']):
            i+=1            
                        
        if i<len(vertices[last]):
            DFSstack.append(vertices[last][i])
        else:
            done_with=DFSstack.pop()
            if not second_pass:
                finish_order.append(done_with)
                
def DFS_loop(vertices, second_pass=False):
    global source
    vlist=finish_order if second_pass else range(len(vertices))
    for i in reversed(vlist):
        if not flags[i]['explored']:
            source=i
            DFS(vertices, i, second_pass)
            
#--------------------------------------------Strongly Connected Components---------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def getSCC(filename):

#---First pass:
    vertices=loadgraph(filename+'.reversed')    
    initialize_flags(len(vertices))
    DFS_loop(vertices)

#---Second pass:
    vertices=loadgraph(filename)
    initialize_flags((len(vertices)))
    DFS_loop(vertices, second_pass=True)

#---Recover SCC (I'm doing another loop over vertices here, which can easily be avoided with some optimization).
    #At least is still linear time.
    SCCs={}
    for vertex in flags:
        SCCs.setdefault(vertex['source'], []).append(vertex)                            #group vertices by source
    print "The ten biggest strongly connected components are:"
    for source in sorted(SCCs.keys(), key=lambda x : len(SCCs[x]), reverse=True)[:10]:  #sort by length of group
        print 'SCC with source %d: size %d' %(source, len(SCCs[source]))
        
    
            

     
#-------------------------------------------------------Main-----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def main():
    getSCC('/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/SCC.txt')
    
if __name__=='__main__':
    main()
