% Interpolation von Framedrops in Zeit und Raum
function fix_input_data = time_fixer(input_data,frame_rate)
diff_time = diff(input_data(:,1));
refresh_rate = 1/frame_rate;

% Breite des Mittelungsfensters
window_size = 5;

%% anhand des Abstandes zwischen Frames leere Zeilen einfügen.
% Z.B. bei 0.010 wird 1 Zeile hinzugefügt, bei 0.015 zwei Zeilen (bei 200 Hz).
% Der zeitliche Abstand wird mit einer Toleranz von 0.0001 bestimmt.
insert_index = [];    
insert_num = [];
for i = 1:10
    insert_index_part = find((diff_time>(refresh_rate*(i+1)-0.0001)) & (diff_time<(refresh_rate*(i+1)+0.0001)));

    insert_num = [insert_num;ones(length(insert_index_part),1)*i]; 

    insert_index = [insert_index;insert_index_part];
end
% Sortiere die einzufügenden Zeilen in aufsteigender Index Reihenfolge
sort_mat = sortrows([insert_index+1,insert_num]);
% Zeilen einfügen
fix_input_data = insert_row(input_data,sort_mat(:,1),sort_mat(:,2));

%% Leerstellen interpolieren
nanind = [0;find(isnan(fix_input_data(:,1)))];

for i = 2:length(nanind)
    % Zeitlichen Verlauf 'auffüllen'
    fix_input_data(nanind(i),1) = fix_input_data(nanind(i)-1,1) + refresh_rate;
    
    % räumlichen Verlauf mit Mittelwert über window_size füllen
    mean_nanind = nan(window_size,1);
    for j=1:window_size
        mean_nanind(j,1) = nanind(i)+(j-ceil(window_size/2));
        if mean_nanind(j,1)>size(fix_input_data,1)
            mean_nanind(j,:) = [];
            break
        end
    end
    fix_input_data(nanind(i),4:6) = nanmean(fix_input_data(mean_nanind(:,1),4:6));
end
end