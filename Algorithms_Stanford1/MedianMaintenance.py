# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:35:16 2013

@author: ste
"""

#------------------------------------------------------------------------The heap-----------------------------------------------------------------

def bubbledown(heap, start):
    if 2*start+2 < len(heap):        #start has 2 children
        minchild = 2*start+1 if heap[2*start+1]<heap[2*start+2] else 2*start+2
        if heap[minchild]<heap[start]:
            heap[minchild], heap[start] = heap[start], heap[minchild]
            bubbledown(heap, minchild)
    if 2*start+1 == len(heap)-1:      #start has one child
        if heap[2*start+1]<heap[start]:
            heap[2*start+1], heap[start] = heap[start], heap[2*start+1]
            
def bubbleup(heap, start):
    if start > 0:
        parent = int((start-1)/2)
        if heap[start]<heap[parent]:
            heap[parent], heap[start] = heap[start], heap[parent]
            bubbleup(heap, parent)
            
def extractmin(heap):
    heap[0], heap[-1] = heap[-1], heap[0]
    minimum = heap.pop()
    bubbledown(heap, 0)
    return minimum

def insert(heap, value):
    heap.append(value)
    bubbleup(heap, len(heap)-1)

def heapify(alist):
    start = int((len(alist)-2)/2)
    while(start>=0):
        bubbledown(alist, start)
        start-=1

#-------------------------------------------------------------------------Medians-----------------------------------------------------------------

#The median is the min element of the right heap. The each insersion we rebalance the heaps so that either
#len(heapright) = len(heapleft)+1 or len(heapright) = len(heapleft)+2

def balance(heapleft, heapright):
    while(len(heapright)>len(heapleft)+2):
        x = extractmin(heapright)
        insert(heapleft, -x)
    while(len(heapleft)>len(heapright)-1):
        x = -extractmin(heapleft)
        insert(heapright, x)


def medians(inputlist):
    heapright=[inputlist[0]]
    heapleft=[]
    medians=[inputlist[0]]
    for el in inputlist[1:]:
        if el<medians[-1]:
            insert(heapleft, -el)
        else:
            insert(heapright, el)  
        balance(heapleft, heapright)
        medians.append(heapright[0])
    
    return medians




#--------------------------------------------------------------------------Test-------------------------------------------------------------------
#
#alist = [8, 9, 24, 99, -34, -2, -9, -66, 9, 38, 630, 91, 11, 1, 23, -76]
#
#for m in medians(alist):
#    print m


with open('/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/Median.txt') as inputfile:
    numbers = [int(line) for line in inputfile]

med = medians(numbers)
for median in med:
    print median
print sum(med)%10000
    
    