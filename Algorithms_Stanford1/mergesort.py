# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/Users/ste/.spyder2/.temp.py
"""

def mergesort(alist):
    if len(alist)<2:
        return
    
    k=int(len(alist)/2)
    firsthalf=alist[:k]
    secondhalf=alist[k:]
    mergesort(firsthalf)
    mergesort(secondhalf)
    i, j, dim1, dim2 = 0, 0, len(firsthalf), len(secondhalf)
    for l in range(0, len(alist)):
        if not i<dim1:
            alist[l]=secondhalf[j]
            j+=1
        elif not j<dim2:
            alist[l]=firsthalf[i]
            i+=1
        elif firsthalf[i]<secondhalf[j]:
            alist[l]=firsthalf[i]
            i+=1
        else:
            alist[l]=secondhalf[j]
            j+=1

mylist=[3, 2, 6, 9, 3, 5, 15, 99, 256, -2, -3]
mergesort(mylist)
print mylist