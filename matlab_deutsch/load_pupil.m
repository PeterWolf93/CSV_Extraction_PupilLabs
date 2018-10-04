% Lädt die von Pupil Player exportierte .csv vollständig als Matlab Struct
% und die interessanten Teile als Matrix ein. Die Info Datei, die die
% Synchronisation enthält wird ebenfall geladen.
function output = load_pupil(directory,file_date,file_num,csv_data_input,...
    info_input,fix_time,frame_rate,denoise,calc_unix) % info hier auch laden

% Dateipfad entsprechend angepassen
data_path = [directory file_date '\' file_num '\'];

%% Laden der Augenposition und Info
% Augendaten werden hier vollständig als Struct geladen
eyes_both = table2struct(readtable([data_path 'exports\' csv_data_input]));

% info Datei wird als Struct geladen
info = array2table(table2array(readtable([data_path info_input]))');
info.Properties.VariableNames = regexprep(table2array(info(1,:)), '\W', '');
info(1,:)=[];
info = table2struct(info);
info.StartTimeSystem = str2double(info.StartTimeSystem);
info.StartTimeSynced = str2double(info.StartTimeSynced);

%% Augen trennen
% Linkes und rechtes Auge getrennt speichern
id=[eyes_both.id];

eyes_id0 = eyes_both(id==0);
eyes_id1 = eyes_both(id==1);

%% Zeit auf Aufnahmestart umrechnen
% Neben dem Start der Aufnahme werden hier die Interessanten Informationen
% des Eyetreckers gespeichert: Frame der Weltkamera, Konfidenz, x- und
% y-Position des Augen, Pupillendurchmesser
ticnd_id0(:,1) = [eyes_id0.timestamp]-info.StartTimeSynced;
ticnd_id0(:,2) = [eyes_id0.index];
ticnd_id0(:,3) = [eyes_id0.confidence];
ticnd_id0(:,4) = [eyes_id0.norm_pos_x];
ticnd_id0(:,5) = [eyes_id0.norm_pos_y];
ticnd_id0(:,6) = [eyes_id0.diameter];

ticnd_id1(:,1) = [eyes_id1.timestamp]-info.StartTimeSynced;
ticnd_id1(:,2) = [eyes_id1.index];
ticnd_id1(:,3) = [eyes_id1.confidence];
ticnd_id1(:,4) = [eyes_id1.norm_pos_x];
ticnd_id1(:,5) = [eyes_id1.norm_pos_y];
ticnd_id1(:,6) = [eyes_id1.diameter];

%% Zeitverlauf reparieren/ annähern
% Falls gewünscht (EMPFOHLEN, SONST FUNKTIONIERT REST NICHT) werden hier Framedrops interpoliert.
if fix_time == 1
    
    % Frames vor Synchronisation löschen
    ticnd_id0(ticnd_id0(:,1)<(-1/(1*frame_rate)),:)=[];
    ticnd_id1(ticnd_id1(:,1)<(-1/(1*frame_rate)),:)=[];

    % 1. Frame (der mit dem geringsten Abstand zur Null) für jedes Auge
    % suchen und als Baseline verwenden
    [~,min_id0] = min(abs(ticnd_id0(1:2,1)));
    [~,min_id1] = min(abs(ticnd_id1(1:2,1)));

    ticnd_id0(:,1) = ticnd_id0(:,1)-ticnd_id0(min_id0,1);
    ticnd_id1(:,1) = ticnd_id1(:,1)-ticnd_id1(min_id1,1);
    
    ticnd_id0(ticnd_id0(:,1)<0,:)=[];
    ticnd_id1(ticnd_id1(:,1)<0,:)=[];
    
    % fehlende Frames interpolieren
    fix_ticnd_id0 = time_fixer(ticnd_id0,frame_rate);
    fix_ticnd_id1 = time_fixer(ticnd_id1,frame_rate); 
    
    % Ende angleichen, überzählige Frames werden gelöscht
    [len_all,len_ind]=min([length(fix_ticnd_id0),length(fix_ticnd_id1)]);
    
    if len_ind == 1
        fix_ticnd_id1(len_all+1:end,:)=[];
    elseif len_ind == 2
        fix_ticnd_id0(len_all+1:end,:)=[];
    end
    
    ticnd_id0 = fix_ticnd_id0;
    ticnd_id1 = fix_ticnd_id1;    
end

% Geschwindigkeit in x- und y-Richtung berechen.
% HIER NOCH ### NICHT ### IN EINHEITEN DES SEHWINKELS!!!
ticnd_id0(:,7) = [0;diff(ticnd_id0(:,4))]/frame_rate;
ticnd_id0(:,8) = [0;diff(ticnd_id0(:,5))]/frame_rate;

ticnd_id1(:,7) = [0;diff(ticnd_id1(:,4))]/frame_rate;
ticnd_id1(:,8) = [0;diff(ticnd_id1(:,5))]/frame_rate;

% tatsächlich gemessene mittlere FPS nach time_fix
real_fps_id0 = 1/mean(diff(ticnd_id0(:,1)));
real_fps_id1 = 1/mean(diff(ticnd_id1(:,1)));

% FPS mit Framedrops berechnen
timestamp_id0 = [eyes_id0.timestamp];
timestamp_id1 = [eyes_id1.timestamp];

time_id0 = timestamp_id0(end) - timestamp_id0(1);
time_id1 = timestamp_id1(end) - timestamp_id1(1);

drop_fps_id0 = size(timestamp_id0,2)/time_id0;
drop_fps_id1 = size(timestamp_id1,2)/time_id1;


%% Signal entrauschen
if denoise == 1
    try
        evalc('dwtmode(''per'')');
        threshold = 'minimaxi';
%         threshold = 'sqtwolog';
        SORH = 'h';
        SCAL = 'sln';
        N = 4;
        wname = 'sym8';        
        for i = 4:5
            ticnd_id0(:,i) = wden(ticnd_id0(:,i),threshold,SORH,SCAL,N,wname);
            
            ticnd_id1(:,i) = wden(ticnd_id1(:,i),threshold,SORH,SCAL,N,wname);
        end
    catch
        warning('no wavelet toolbox available')
    end
end

%% Zeit auf Unix umrechnen
if calc_unix == 1
    ticnd_id0(:,1) = ticnd_id0(:,1) + info.StartTimeSystem;
    ticnd_id1(:,1) = ticnd_id1(:,1) + info.StartTimeSystem;
end

%% Ausgabe
output.id0.capturedata = eyes_id0;
output.id1.capturedata = eyes_id1;

output.id0.eyedata = ticnd_id0;
output.id1.eyedata = ticnd_id1;

output.id0.rel_framedrops = 1-size(eyes_id0,1)/size(ticnd_id0,1);
output.id1.rel_framedrops = 1-size(eyes_id1,1)/size(ticnd_id1,1);

output.id0.abs_framedrops = size(ticnd_id0,1)-size(eyes_id0,1);
output.id1.abs_framedrops = size(ticnd_id1,1)-size(eyes_id1,1);

output.id0.drop_fps = drop_fps_id0;
output.id1.drop_fps = drop_fps_id1;

output.id0.real_fps = real_fps_id0;
output.id1.real_fps = real_fps_id1;

output.capturedata = eyes_both;
output.info = info;
output.timefix = fix_time;
end