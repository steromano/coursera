# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 11:35:29 2013

@author: ste
"""


#
#myhashtable={}
#for k in range(-999999, 1000000):
#    myhashtable[k]=[]

from collections import defaultdict

myhashtable = defaultdict(list)    

with open('/Users/ste/Desktop/Ste/Python/AlgorithmsCourse/2sum.txt') as inputfile:
    for line in inputfile:
        n=int(line)
        hashv = int(n/1000000)
        myhashtable[hashv].append(n)
        


for hashv, bucket in myhashtable.iteritems():
    if -hashv in myhashtable and -hashv-1 in myhashtable and -hashv-2 in myhashtable:
        print hashv, bucket
        print -hashv, myhashtable[-hashv]
        print -hashv-1, myhashtable[-hashv-1]
        print -hashv-2, myhashtable[-hashv-2]
        print '\n\n'
        
#for hashv, bucket in myhashtable.iteritems():
#    print hashv, bucket

twosums = []
for xhash in myhashtable:
#    counting+=1
#    print counting
    ybucket=[]
    if -xhash in myhashtable:
        ybucket+=myhashtable[-xhash]
    if -xhash-2 in myhashtable:
        ybucket+=myhashtable[-xhash-2]
    if -xhash-1 in myhashtable:
        ybucket+=myhashtable[-xhash-1]
    for x in myhashtable[xhash]:
        for y in ybucket:
            s = x + y
            if s>= -10000 and s <= 10000 and s not in twosums and x!= y:
                twosums.append(s)
                #print '%d + %d = %d' %(x, y, s)
print len(twosums)
            


#The brutest of the forces (takes about 3 hours):
#
#
#'numbers' here is a set to avoid duplicates.
#count = 0
#
#for k in range(-10000, 10001):
#    print k
#    for number in numbers:
#        if k-number in numbers:
#            count+=1
#            break
#    
#print count            #----> result = 427


