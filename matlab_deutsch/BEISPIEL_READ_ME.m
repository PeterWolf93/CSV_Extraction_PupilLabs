% hier steht der Speicherort der Messdaten: z.B. 
% directory = 'C:\Users\NAME\Desktop\Pupil_VR_Recordings\'];
directory = '';

% Datum und Nummer der Aufnahme. Nach der Extraktion darauf achten, dass
% die 'pupil_positions.csv' Datei direkt im Ordner 'exports' leigt.
file_date = '2018_09_04';
file_num = '000';

% Es wird empfohlen Framedrops vor weiterer Verwendung der Daten zu
% Interpolieren:
fix_time = 1;

% Bei der Aufnahme eingestelle Bildwiederholrate hier angeben
set_fps = 120;

% Sollen die Daten noch mit einem Denoise Filter bearbeitet werden?
% Benötigt wavelet toolbox.
denoise = 0;

% Zeitpunkte Relativ zum auf Aufnahmestart oder zur Unix Zeit darstellen.
calc_unix = 0;

csv_data = load_pupil(directory,file_date,file_num,'pupil_positions.csv',...
    'info.csv',fix_time,set_fps,denoise,calc_unix);