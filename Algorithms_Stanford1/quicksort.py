# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:49:17 2013

@author: ste
"""
import random
from math import log

#The stupid quicksort does not work in place, it allocates two new arrays in each call instead
def stupid_quicksort(array):
    if len(array)<2:
        return array
    #print "input array: ", array
    i = random.randrange(len(array))
    pivot=array.pop(i)
    less, more= [], []
    for el in array:
        if el<= pivot:
            less.append(el)
        else:
            more.append(el)
    return stupid_quicksort(less)+[pivot]+stupid_quicksort(more)


#The true quicksort does its job in place by repeatedly switching pair of elements of the array

def switch(array, i, j):            #Switch elements i and j of the input array
    if i==j:
        return
    temp= array[i]
    array[i]=array[j]
    array[j]=temp    

def setpivot(array, left, right, mode = 'r'):      #Modes are: 'r' for random (default), 'f' for first, 'l' for last, 
    if mode == 'r':                                #'m' for median of first, last and middle
        return random.randrange(left, right)
    elif mode == 'f':
        return left
    elif mode == 'l':
        return right-1
    elif mode == 'm':
        mid=int((right-left-1)/2+left)
        if array[left]<array[right-1]:
            if array[mid]<array[left]:
                return left
            elif array[right-1]<array[mid]:
                return right-1
            else:
                return mid
        else:
            if array[mid]<array[right-1]:
                return right-1
            elif array[left]<array[mid]:
                return left
            else:
                return mid
    else:
        print "Unexisting mode. Using default."
        setpivot(array, left, right)
        


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

    

    
#Let's count the comparison that the algorithm makes:
comparisons=0
    
def quicksort(array, left, right):
#Trivial base case
    if right-left<2:
        return
        
#Set the pivot        
    pivot_index=setpivot(array, left, right, 'f')
    switch(array, left, pivot_index)

#Partition
    i=partition(array, left, right)

#Divide & Conquer
    quicksort(array, left, i-1)
    quicksort(array, i, right)
    
            
          
    
to_sort=[]
def loadarray():
    global to_sort
    to_sort=[]
    with open("/Users/ste/Desktop/Ste/C++/Programs/AlgorithmCourse/quicksort/quicksort/QuickSort.txt") as bigarray:
        for number in bigarray:
            to_sort.append(int(number.strip('\r\n')))


        
loadarray()
#quicksorted = stupid_quicksort(to_sort)
quicksort(to_sort, 0, 900)

#with open("/Users/ste/Desktop/Ste/Python/Esercizi/output.txt", "w") as output:
#    for j in to_sort:
#        output.write(str(j)+'\n')
print "Sorted!"
print "Comparisons made:", comparisons
print "Comparison/(nlogn)=", comparisons/(len(to_sort)*log(len(to_sort)))


#Now, to compare with the worst case scenario of quicksort, run it again on the sorted array by using the first element
#as the pivot. Decomment the below and comment the lines above where the pivot is randomized. Also, the full 100000-
#size is too large appaently to run the worst case scenario on it. Limit the size of the input using by calling
#quicksort on a subarray instead of the full array.

comparisons=0
quicksort(to_sort, 0, 900)
print "Sorted!"
print "Comparisons made:", comparisons
print "Comparison/(nlogn)=", comparisons/(len(to_sort)*log(len(to_sort)))