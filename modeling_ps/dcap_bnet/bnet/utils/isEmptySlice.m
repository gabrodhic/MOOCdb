function [ bool ] = isEmptySlice( slice )
% input cell is a n x 1 cell where each element is either [] or a number
% return 1 if all elements are empty []
% else return 0

bool = 1;

ncells = size(slice,1);

for i=1:ncells
    if ~(isempty(slice{i,1}))
        bool = 0;
        break
    end


end

