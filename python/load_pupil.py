# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 08:42:45 2018

@author: P. Wolf

title: load_pupil

"""
#%% Imports
import pandas as pd
import numpy as np
from time_fixer import time_fixer
from movingmean import movingmean

#%% Output
class PupilReturnValue(object):
    def __init__(self, eyes_id0, eyes_id1, ticnd_id0, ticnd_id1, real_fps_id0, 
                 real_fps_id1, drop_fps_id0, drop_fps_id1, eyes_both, info, fix_time):
        self.id0_capturedata = eyes_id0
        self.id1_capturedata = eyes_id1
        
        self.id0_eyedata = ticnd_id0
        self.id1_eyedata = ticnd_id1
        
        self.id0_rel_framedrops = 1-np.size(eyes_id0,1)/np.size(ticnd_id0,1)
        self.id1_rel_framedrops = 1-np.size(eyes_id1,1)/np.size(ticnd_id1,1)
        
        self.id0_abs_framedrops = np.size(ticnd_id0,1)-np.size(eyes_id0,1)
        self.id1_abs_framedrops = np.size(ticnd_id1,1)-np.size(eyes_id1,1)
        
        self.id0_real_fps = real_fps_id0
        self.id1_real_fps = real_fps_id1
        
        self.id0_drop_fps = drop_fps_id0
        self.id1_drop_fps = drop_fps_id1
        
        self.capturedata = eyes_both
        self.info = info
        self.timefix = fix_time

#%% main function
def load_pupil(directory, file_date, file_num, csv_data_input, info_input, 
               fix_time, frame_rate, use_filter, window_size):
    
    # Path to the data we want to load
    data_path = directory + file_date + '\\' + file_num + '\\'
    
    #%% Load eye_data and info
    eyes_both = pd.read_csv(data_path + 'exports\\' + csv_data_input, delimiter=',')
    info_temp = pd.read_csv(data_path + info_input, delimiter=',')
    info_temp2 = info_temp.T
    info_temp2.columns = info_temp2.iloc[0]
    info = info_temp2.drop(info_temp2.index[0])
    
    #%% extract eye_data and seperate left from right    
    eyes_id0 = eyes_both.loc[eyes_both['id'] == 0]
    eyes_id1 = eyes_both.loc[eyes_both['id'] == 1]
    
    #%% convert to array and align start time
    ticnd_id0 = np.ndarray((np.size(eyes_id0,0), 8))
    ticnd_id0[:,0] = np.asarray(eyes_id0.timestamp) - \
        float(np.asarray(info.loc[:,'Start Time (Synced)']))
    ticnd_id0[:,1] = np.asarray(eyes_id0.index)
    ticnd_id0[:,2] = np.asarray(eyes_id0.confidence)
    ticnd_id0[:,3] = np.asarray(eyes_id0.norm_pos_x)
    ticnd_id0[:,4] = np.asarray(eyes_id0.norm_pos_y)
    ticnd_id0[:,5] = np.asarray(eyes_id0.diameter)
    
    ticnd_id1 = np.ndarray((np.size(eyes_id1,0), 8))
    ticnd_id1[:,0] = np.asarray(eyes_id1.timestamp) - \
        float(np.asarray(info.loc[:,'Start Time (Synced)']))
    ticnd_id1[:,1] = np.asarray(eyes_id1.index)
    ticnd_id1[:,2] = np.asarray(eyes_id1.confidence)
    ticnd_id1[:,3] = np.asarray(eyes_id1.norm_pos_x)
    ticnd_id1[:,4] = np.asarray(eyes_id1.norm_pos_y)
    ticnd_id1[:,5] = np.asarray(eyes_id1.diameter)
    
    #%% fix framedrops
    if fix_time == 1:
        # delete frames which occured before sync
        mask_id0 = ticnd_id0[:,0]>(-1/(1*frame_rate))
        ticnd_id0 = ticnd_id0[mask_id0,...]
        
        mask_id1 = ticnd_id1[:,0]>(-1/(1*frame_rate))
        ticnd_id1 = ticnd_id1[mask_id1,...]
        
        # the frame closest to t=0 becomes t_0, delete earlier frames
        min_id0 = np.argmin(abs(ticnd_id0[:,1:2]))
        min_id1 = np.argmin(abs(ticnd_id1[:,1:2]))
        
        ticnd_id0[:,0] = ticnd_id0[:,0]-ticnd_id0[min_id0,0]
        ticnd_id1[:,0] = ticnd_id1[:,0]-ticnd_id1[min_id1,0]
        
        mask_id0 = ticnd_id0[:,0]>=0
        ticnd_id0 = ticnd_id0[mask_id0,...]
        
        mask_id1 = ticnd_id1[:,0]>=0
        ticnd_id1 = ticnd_id1[mask_id1,...]
        
        # add back dropped frames
        fix_ticnd_id0 = time_fixer(ticnd_id0,frame_rate)
        fix_ticnd_id1 = time_fixer(ticnd_id1,frame_rate)
        
        # cut of overlapping frames
        len_both = [len(fix_ticnd_id0),len(fix_ticnd_id1)]
        len_ind = np.argmin(len_both)
        len_all = np.min(len_both)
        
        if len_ind == 0:
            fix_ticnd_id0 = np.delete(fix_ticnd_id0, 
                                      list(range(len_all+1,len_both[0])), axis=0)
        elif len_ind == 1:
            fix_ticnd_id1 = np.delete(fix_ticnd_id1, 
                                      list(range(len_all+1,len_both[1])), axis=0)
        
        ticnd_id0 = fix_ticnd_id0
        ticnd_id1 = fix_ticnd_id1
        
    # calculate velocity in x and y direction in units of the eyetracker
    ticnd_id0[:,6] = np.append(0, np.diff(ticnd_id0[:,4])/frame_rate)
    ticnd_id0[:,7] = np.append(0, np.diff(ticnd_id0[:,5])/frame_rate)

    ticnd_id1[:,6] = np.append(0, np.diff(ticnd_id1[:,4])/frame_rate)
    ticnd_id1[:,7] = np.append(0, np.diff(ticnd_id1[:,5])/frame_rate)
    
    # calculate mean FPS after use of time_fix
    real_fps_id0 = 1/np.mean(np.diff(ticnd_id0[:,0]))
    real_fps_id1 = 1/np.mean(np.diff(ticnd_id1[:,0]))
    
    # calculate mean FPS with framedrops
    timestamp_id0 = np.asarray(eyes_id0.timestamp)
    timestamp_id1 = np.asarray(eyes_id1.timestamp)
    
    time_id0 = timestamp_id0[-1] - timestamp_id0[0]
    time_id1 = timestamp_id1[-1] - timestamp_id1[0]
    
    drop_fps_id0 = np.size(timestamp_id0,0)/time_id0
    drop_fps_id1 = np.size(timestamp_id1,0)/time_id1
    
    #%% filter eye_data
    if use_filter == 1 and window_size > 0:
        ticnd_id0[:,3] = movingmean(ticnd_id0[:,3],window_size)
        ticnd_id0[:,4] = movingmean(ticnd_id0[:,4],window_size)
        
        ticnd_id1[:,3] = movingmean(ticnd_id1[:,3],window_size)
        ticnd_id1[:,4] = movingmean(ticnd_id1[:,4],window_size)
        
    return PupilReturnValue(eyes_id0, eyes_id1, ticnd_id0, ticnd_id1, real_fps_id0, 
                            real_fps_id1, drop_fps_id0, drop_fps_id1, eyes_both, 
                            info, fix_time)
