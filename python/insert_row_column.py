# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:38:20 2018

@author: P. Wolf

title: insert_row
"""
#%% Imports
import numpy as np

#%%
def insert_row(input_matrix,insert_index,insert_num):
    new_matrix = input_matrix
    
    for i in range(len(insert_index)):
        z = np.zeros((insert_num[i],np.size(input_matrix,1)))
        z.fill(np.nan)
        new_matrix = np.insert(new_matrix,insert_index[i],z,0)
        insert_index = insert_index + insert_num[i]
        
    return new_matrix

#%%
def insert_column(input_matrix,insert_index,insert_num):
    new_matrix = input_matrix
    
    for i in range(len(insert_index)):
        z = np.zeros((np.size(input_matrix,1),insert_num[i]))
        z.fill(np.nan)
        new_matrix = np.insert(new_matrix,insert_index[i],z,1)
        insert_index = insert_index + insert_num[i]
        
    return new_matrix