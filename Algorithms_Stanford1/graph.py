# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:01:44 2013

@author: ste
"""

import networkx as nx
import matplotlib.pyplot as plt


#Takes as input the graph in the form a list of edges, each represented as a pair of integers
#(each integer is a node), and draws it. Cool stuff.

def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges  
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    nx.draw(G)

    # show graph
    plt.show()

graph=[]
with open("/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/mincuttest.txt") as inputgraph:
    for line in inputgraph:
        node=line.split()
        for adjacent in node[1:]:
            graph.append((node[0], adjacent))

draw_graph(graph)
        