# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 09:05:33 2018

@author: P. Wolf

title: time_fixer
"""
#%% Imports
import numpy as np
import math as mat
from insert_row_column import insert_row

#%%
def time_fixer(input_data,frame_rate):
    diff_time = np.diff(input_data[:,0])
    refresh_rate = 1/frame_rate
    
    # size of averageing window
    window_size = 5
    
    #%% insert columns if framedrop occured
    insert_index = np.asarray([])
    insert_num = np.asarray([])
    for i in range(1,10):
        insert_index_part = np.asarray(np.where((diff_time>(refresh_rate*(i+1)-0.0001)) & (diff_time<(refresh_rate*(i+1)+0.0001))))
        
        insert_num = np.append(insert_num,[np.ones((np.size(insert_index_part,1),1))*i])
        
        insert_index = np.append(insert_index,[insert_index_part])
        
    # sort in ascending order
    sort_mat = np.sort(np.hstack(((insert_index.reshape(len(insert_index),1))+1,insert_num.reshape(len(insert_index),1))),axis = 0)
    sort_mat = sort_mat.astype(int)
    # insert new rows
    fix_input_data = insert_row(input_data,sort_mat[:,0],sort_mat[:,1])
    
    #%% interpolate frame drops
    nanind = np.argwhere(np.isnan(fix_input_data[:,0]))
    for i in nanind:
        # fill timeline
        fix_input_data[i,0] = fix_input_data[i-1,0] + refresh_rate
        
        # fill positions
        mean_nanind = np.ndarray((window_size,1))
        for j in range(window_size):
            mean_nanind[j] = i + 1 + (j - mat.ceil(window_size/2))
            if mean_nanind[j] > np.size(fix_input_data,0):
                mean_nanind[j,:] = []
            mean_nanind = mean_nanind.astype(int)
        
        check_size = mean_nanind < np.size(fix_input_data,0)
        if False in check_size:
            mean_nanind = mean_nanind[check_size]
            mean_nanind = mean_nanind.reshape(np.size(mean_nanind),1)
        
        fix_input_data[i,3:6] = np.nanmean(fix_input_data[mean_nanind[:,0],3:6], axis = 0)
        
    return fix_input_data

#a = np.ndarray((10,2))
##a[:,0]=np.asarray(range(100,110))
#a[0:5,0]=np.asarray(range(0,5))
#a[5:10,0]=np.asarray(range(6,11))
#a[7:10,0]=np.asarray(range(9,12))
#a[:,1]=np.asarray(range(10,20))
#
#b = time_fixer(a,1)
