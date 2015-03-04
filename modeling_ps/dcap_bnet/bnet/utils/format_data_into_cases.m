% Created on: 2/27/2014
% Last modified: 5/9/2014
% Author: Elaine Han (skewlight@gmail.com)

% Put formatted input data (uniform format for ALL purposes) into cell
% cases. Input data to this function is the output formatted data from the
% format_data_for_problems_csv function. The output cases will be used for
% training and testing.
% The output 'supports' stores all possible states for the observable
% nodes, which allows us to map from bnet indexes back to specific states
%(see below for detail).
%
% There are 3 more paramters controlling output nodes:
% 1. empty_state: if is 1, consider an empty answer (resource slide) as an
%                 extra answer node state (e.g. 11) instead of leaving it
%                 as empty
% 2. empty_res: if is 1, consider an empty resource (answer slide) as an
%               extra resource node state instead of leaving it as empty
% 3. binary: if is 1, make answer node binary (all wrong answers become
%            state 2)
function [cases, supports] = format_data_into_cases(data, max_num_of_slices, nodes_per_slice, empty_state, empty_res, binary)

% Complete data (before we divide data for CV) in format
% user_id, observable node 1,  observable node 2, ....

% nodes per slice£¬ this should match number of columns in data
assert(nodes_per_slice == size(data,2), 'Number of column does not match nodes_per_slice');

% node 1 = hidden node
% node 2:nodes_per_slice = observable nodes

users = unique(data(:,1)); % list of unique users
ncases = size(users,1); % number of unique users, also the number of output cases

%% ------Outputs ------
% cases = 1 x (number of cases) of cases where
% each case is a (slice size) x (number of slices cell) matrix.
cases = cell(1,ncases);

%% 'supports' stores all possible states for each observable nodes.
% e.g. if we have unique resource ids [23,344,1666], they will be referenced
% by their index [1,2,3] in bnet. The supports variable will allow us to map from
% index 2 back to the corresponding resource id 344.
supports = cell(1,nodes_per_slice-1); 
% ------------------------
%% Fill up all possible state for each node, excluding 0 which
%means we will leave the node/element empty instead of filling in a state
for node=1:nodes_per_slice-1
    supports{node} = unique(data(data(:,node+1)~= 0 ,node+1));
end

%% make empty answer an extra answer node state (e.g. 11 in this case).
if (empty_state == 1)
    EMPTY_ANSWER = size(supports{2},1)+1;
    supports{2}(EMPTY_ANSWER) = 0;
end	

%% make answer binary.
%fprintf('binary is %i',binary);
if (binary == 1)
    supports{2} = transpose(1:2);
end

%% make empty resource an extra resource node state. Resource has +1 support.
if (empty_res == 1)
    EMPTY_RESOURCE = size(supports{1},1)+1;
    supports{1}(EMPTY_RESOURCE) = 0;
end

%% fill up cases
for u=1:ncases
	userdata = data(data(:,1) == users(u),:); %all lines of data related to this user
	
	cases{u} = cell(nodes_per_slice, max_num_of_slices);

	for slice = 1:min(size(userdata,1),max_num_of_slices)
        for node = 2:nodes_per_slice
            if (userdata(slice,node) ~= 0)
                cases{u}(node,slice) = num2cell(find(supports{node-1} == userdata(slice,node)));
            end

            % make empty resource (answer slide) a last state for res node
            if (empty_res == 1)
                if (node == 2) && (userdata(slice, node) == 0)
                    cases{u}(node,slice) = num2cell(EMPTY_RESOURCE);
                end
            end
	    
            % make empty answer (resource slide) a last state (e.g. 11) for ans node
            if (empty_state == 1)
                if (node == 3) && (userdata(slice, node) == 0)
                    cases{u}(node,slice) = num2cell(EMPTY_ANSWER);
                end
            end
            
            % make answers binary, fill in state 2 for incorrect answers.
            if (binary == 1)
                if (node == 3) && (userdata(slice,node) > 1)
                    cases{u}(node,slice) = num2cell(2);
                end
            end
        end        
	end
end	


