% Fügt bei den genannten Stellen eine leere Zeile ein. Die Indizes beziehen
% sich immer auf die Position der Zeile VOR jeglichem Einfügen. Als Bsp:
% A = magic(4)
% A = 16     2     3    13
%      5    11    10     8
%      9     7     6    12
%      4    14    15     1

% B = insert_column(A,2,1)
% B = 16   NaN     2     3    13
%      5   NaN    11    10     8
%      9   NaN     7     6    12
%      4   NaN    14    15     1

function output = insert_column(input_matrix,insert_index,insert_num)

new_matrix = input_matrix;

for i = 1:length(insert_index)
    insert_matrix=nan(size(input_matrix,1),insert_num(i));
    new_matrix = [new_matrix(:,1:insert_index(i)-1) insert_matrix new_matrix(:,insert_index(i):end)];
    insert_index = insert_index + insert_num(i);
end

output = new_matrix;

end