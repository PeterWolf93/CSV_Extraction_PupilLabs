% directory of the data ypu want to load into Matlab: eg.
% directory = 'C:\Users\NAME\Desktop\Pupil_VR_Recordings\'];
directory = '';

% Date and number of the recording. After you use the data exporter from
% pupil_player you have to move 'pupil_positions.csv' from the folder with
% the exported frames directly to the 'exports' folder.
file_date = '2018_09_04';
file_num = '000';

% interpolate framedrops
fix_time = 1;

% set the frame frequency you used for recording
set_fps = 120;

% set to 1 if you want to use a denoise filter. requires wavelet toolbox.
denoise = 0;

% display timeline relative to the recording onset or unix time
calc_unix = 0;

csv_data = load_pupil(directory,file_date,file_num,'pupil_positions.csv',...
    'info.csv',fix_time,set_fps,denoise,calc_unix);
