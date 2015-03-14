# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 20:12:12 2013

@author: ste
"""

import random

def switch(array, i, j):
    if i==j:
        return
    array[i], array[j] = array[j], array[i]

comparisons=0
    
def partition(array, left, right):              #Partitions array[left+1:right] around array[left]
    i=left+1
    for j in range(left+1, right):
        if array[j]<array[left]:     
            switch(array, i, j)            
            i+=1
    switch(array, left, i-1)
    global comparisons
    comparisons+=right-left-1
    return i

def rselect(array, left, right, k):
    pivot_index=random.randrange(left, right)
    switch(array, left, pivot_index)
    i = partition(array, left, right)
    if k > i-1:
        return rselect(array, i, right, k)
    elif k < i-1:
        return rselect(array, left, i-1, k)
    else:
        return array[i-1]

#Test:
#test=[2, 3, 5, 7, 8, 9, 6, 1, 4, 0]

    
test=[]
def loadarray():
    global test
    test=[]
    with open("/Users/ste/Desktop/Ste/C++/Programs/AlgorithmCourse/quicksort/quicksort/QuickSort.txt") as bigarray:
        for number in bigarray:
            test.append(int(number.strip('\r\n')))
        
loadarray()
print rselect(test, 0, len(test), 554)
print "Comparisons made:", comparisons
print "Comparisons/n:", comparisons/float(len(test))
#for k in range(0, len(test)):
#    print rselect(test, 0, len(test), k)