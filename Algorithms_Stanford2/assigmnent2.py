# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 19:29:50 2014

@author: ste
"""

with open("clustering1.txt") as f:
    n = int(f.readline())
    input_edges = [(n1, n2, cost) for (n1, n2, cost) in map(lambda line: map(int, line.split()), f)]

#input_edges = [(1, 2, 1), (1, 3, 1), (1, 4, 100), (1, 5, 100),
#               (2, 3, 2), (2, 4, 50), (2, 5, 80),
#               (3, 4, 70), (3, 5, 60),
#               (4, 5, 1)]

edges = sorted(input_edges, key = lambda (n1, n2, cost): cost)
nodes = set(map(lambda (n1, n2, c): n1, edges) + map(lambda (n1, n2, c): n2, edges))

has_leader = {node: node for node in nodes}
is_leader = {node: [node] for node in nodes}

k = 4
iteration = 0
verbose = False
max_iter = 500

while True:
    (u, v, mincost) = edges.pop(0)
    if verbose:
        print "edge:", (u, v)
        print
    if has_leader[u] == has_leader[v]:
        if verbose:
            print "same cluster"
        continue
    if len(is_leader) == k:
        break
    leader_u, leader_v = has_leader[u], has_leader[v]
    cluster_u, cluster_v = is_leader[leader_u], is_leader[leader_v]
    if verbose: 
        print "Before updating:"
        print
        print "leaders:", leader_u, leader_v
        print "clusters:", cluster_u, cluster_v
    if len(cluster_u) < len(cluster_v):
        for node in cluster_u:
            has_leader[node] = leader_v
        is_leader[leader_v] += cluster_u
        del is_leader[leader_u]
    else:
        for node in cluster_v:
            has_leader[node] = leader_u
        is_leader[leader_u] += cluster_v
        del is_leader[leader_v]
    if verbose:
        print
        print "After updating:"
        print
        print "leaders:", has_leader[u], has_leader[v]
        print "clusters:", is_leader[has_leader[u]], is_leader[has_leader[v]]
        print "--------------------------"
        print
    iteration += 1
    if iteration > max_iter:
        break

print mincost


# Comparison with random clusters    

#def random_clusters(n, k):
#    breaks = [0] + sorted(np.random.choice(range(1, n), k - 1, replace = False)) + [n]
#    perm = np.random.permutation(range(1, n + 1))
#    return [perm[breaks[i]:breaks[i + 1]] for i in range(len(breaks) - 1)]
#    
#clusters = random_clusters(n, k)
#separations = []
#for i in range(len(clusters)):
#    for j in range(i + 1, len(clusters)):
#        print i, j
#        m = min([c for (e1, e2, c) in input_edges if e1 in clusters[i] and e2 in clusters[j] or
#                                                     e2 in clusters[i] and e1 in clusters[j]])
#        separations.append(m)
#
#print(min(separations))




with open("clustering_big.txt") as f:
    n, bits = map(int, f.readline().split())
    nodes = ["".join(line.split()) for line in f]

nodes_dict= {}
for i in range(len(nodes)):
    nodes_dict[nodes[i]] = nodes_dict.get(nodes[i], []) + [i]
    
def Hamming(i, j):
    return sum(map(lambda (x, y): x != y, zip(nodes[i], nodes[j])))

def flip(bit):
    return "0" if bit == "1" else "1"
    
def flip_one(bits):
    return [bits[:i] + flip(bits[i]) + bits[i+1:] for i in range(len(bits))]

def flip_two(bits):
    return [bits[:i] + flip(bits[i]) + bits[i+1:j] + flip(bits[j]) + bits[j+1:]
            for i in range(len(bits)) for j in range(i+1, len(bits))]

d0 = []
d1 = []
d2 = []
for i in range(len(nodes)):
    print i
    d0 += [(i, j) for j in nodes_dict[nodes[i]] if j > i]
    for bits in flip_one(nodes[i]):
        if bits in nodes_dict:
            d1 += [(i, j) for j in nodes_dict[bits] if j > i]  
    for bits in flip_two(nodes[i]):
        if bits in nodes_dict:
            d2 += [(i, j) for j in nodes_dict[bits] if j > i]

has_leader = {i:i for i in range(len(nodes))}
is_leader = {i:[i] for i in range(len(nodes))}

iterations = 0
for (u, v) in d0+d1+d2:
    iterations += 1
    print iterations
    leader_u = has_leader[u]
    leader_v = has_leader[v]
    if leader_u == leader_v:
        continue
    cluster_u = is_leader[leader_u]
    cluster_v = is_leader[leader_v]
    if len(cluster_u) < len(cluster_v):
        for node in cluster_u:
            has_leader[node] = leader_v
        is_leader[leader_v] += cluster_u
        del is_leader[leader_u]
    else:
        for node in cluster_v:
            has_leader[node] = leader_u
        is_leader[leader_u] += cluster_v
        del is_leader[leader_v]
    

def cluster_separation(i, j):
    if has_leader[i] == has_leader[j]:
        return 0
    return min([Hamming(k, l) for k in is_leader[has_leader[i]] for l in is_leader[has_leader[j]]])

















