# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:12:22 2018

@author: P. Wolf

title: movingmean
"""

import numpy as np

def movingmean(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'same')
    return sma

#x = np.asarray([1,2,3,4,5,6,7,8,9,10])
#y = np.asarray([3,5,2,4,9,1,7,5,9,1])
# 
#yMA = movingmean(y,5)
#print(yMA)