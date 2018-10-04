# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 12:45:46 2018

@author: P. Wolf
"""
from load_pupil import load_pupil

# directory of the data ypu want to load into Python: eg.
# directory = 'C:\\Users\\NAME\\Desktop\\Pupil_VR_Recordings\\'];
directory = ''

# Date and number of the recording. After you use the data exporter from
# pupil_player you have to move 'pupil_positions.csv' from the folder with
# the exported frames directly to the 'exports' folder.
file_date = '2018_09_04'
file_num = '000'

# interpolate framedrops
fix_time = 1
window_size = 5

# set the frame frequency you used for recording
set_fps = 120

# set to 1 if you want to use a denoise filter. requires wavelet toolbox.
denoise = 0
use_filter = 0

# display timeline relative to the recording onset or unix time
calc_unix = 0

csv_data = load_pupil(directory, file_date, file_num, 'pupil_positions.csv', 'info.csv', 
                      fix_time, set_fps, use_filter, window_size)

# access output
id0_capturedata = csv_data.id0_capturedata
id1_capturedata = csv_data.id1_capturedata

id0_eyedata = csv_data.id0_eyedata
id1_eyedata = csv_data.id1_eyedata

id0_rel_framedrops = csv_data.id0_rel_framedrops
id1_rel_framedrops = csv_data.id1_rel_framedrops

id0_abs_framedrops = csv_data.id0_abs_framedrops
id1_abs_framedrops = csv_data.id1_abs_framedrops

id0_real_fps = csv_data.id0_real_fps
id1_real_fps = csv_data.id1_real_fps

id0_drop_fps = csv_data.id0_drop_fps
id1_drop_fps = csv_data.id1_drop_fps

capturedata = csv_data.capturedata
info = csv_data.info
timefix = csv_data.timefix