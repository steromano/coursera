# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 17:00:26 2014

@author: ste
"""

C = np.zeros((9, 9))

C[1, 1] = 20
C[2, 2] = 5
C[3, 3] = 17
C[4, 4] = 10
C[5, 5] = 20
C[6, 6] = 3
C[7, 7] = 25

for d in range(1, 7):
    for i in range(1, 7 - d + 1):
        j = i + d
        print i, j
        print [C[i, r-1] + C[r+1, j] for r in range(i, j+1)]
        C[i, j] = min([C[i, r-1] + C[r+1, j] for r in range(i, j+1)]) + \
                  sum([C[k, k] for k in range(i, j+1)])
