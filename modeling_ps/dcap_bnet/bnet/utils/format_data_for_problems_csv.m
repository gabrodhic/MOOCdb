% Created on: 3/6/2014
% Last modified: 3/6/2014
% Author: Elaine Han (skewlight@gmail.com)

% This function format rows of data from problem_%i_v2.csv
% into formatted data:
%   user_id, observable node 1,  observable node 2
%
% - The feature parameter determines whether we use resource id (feature =
%   1) or resource type id (feature = 2).
function [ formatted ] = format_data_for_problems_csv(data, nodes_per_slice, feature)
% output data with dimension: (number of data points) x (nodes per slice)
formatted = zeros( size(data,1), nodes_per_slice);

% first column is always user_id
formatted(:,1) = data(:,1);

%% for this specific problem, we have 2 observable nodes. The input format for each row is:
% For a resource: 1) user_id 2) timestamp 3)resource_id 
%                 4) resource_type_id 5) duration 6) 0
% For an answer:  1) user_id 2) timestamp 3) 0 4) 0 
%                 5) old correctness* 0 or 1 6) 1 for correct,
%                 2+ for different incorrect answers.
% *old correctness is from grading using our own extracted answer key which
%   might contain wrong answers that were marked as correct by edx.

% node 1 = S, hidden student state
% node 2 = R, resource visited 1+
% node 3 = A, answer category 0 = didn't answer 1 = correct 2+ wrong answers

% Feature parameter determines whether we use resource id or resource type
% id.
if (feature == 1)
	formatted(:,2) = data(:,3+1); % use resource id
elseif (feature == 2)
	formatted(:,2) = data(:,4+1); % use resource type id
end
formatted(:,3) = data(:,6+1);

end

