% Created on: 3/6/2014
% Last modified: 3/6/2014
% Author: Elaine

function [ formatted ] = format_data_for_problems_csv( data,nodes_per_slice,feature)

% specific data formatting for problem_%i_v2.csv
% into formatted data:
% user_id, observable node 1,  observable node 2, ....

formatted = zeros( size(data,1), nodes_per_slice);

% first column is always user_id
formatted(:,1) = data(:,1);

% for this specific problem with input data format and 2 observable nodes
% 1) user_id 2) timestamp 3)resource_id 4) resource_type_id 5) duration 6) 0
% 1) user_id 2) timestamp 3) 0 4) 0 5) old correctness (not corrected) 0/1 6) 1 for correct, 2+ for different incorrect answers

% node 1 = S, hidden student state
% node 2 = R, resource visited 1+
% node 3 = A, answer category 0 = didn't answer 1 = correct 2+ wrong answers

%parsing of timestamp returns 2 columns
if (feature==1)
	formatted(:,2) = data(:,3+1); %resource id
elseif (feature==2)
	formatted(:,2) = data(:,4+1); %resource type id
end
formatted(:,3) = data(:,6+1);


end

