# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 19:18:48 2013

@author: ste
"""

a = [-5, -3, 4, 5, 6, 8, 9, 9, 10, 10, 10]


def checkdiag(a):
    i, j = 0, len(a)-1
    while i <= j:
        if a[i]== i or a[j]==j:
            return True
        if a[i]>i:
            i = a[i]
        else:
            i+=1
        if a[j]<j:
            j=a[j]
        else:
            j-=1       
    return False
    
print checkdiag(a)
    