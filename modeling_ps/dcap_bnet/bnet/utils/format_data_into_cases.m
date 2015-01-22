% Created on: 2/27/2014
% Last modified: 5/9/2014
% Author: Elaine

% put input data (uniform format for ALL purposes) into cell cases

function [cases,supports] = format_data_into_cases(data, max_num_of_slices, nodes_per_slice,empty_state,empty_res,binary)

%%
% complete data (before CV) in format
% user_id, observable node 1,  observable node 2, ....

% max_num_of_slices
% nodes per slice£¬ this should match number of columns in data
assert(nodes_per_slice == size(data,2),'Number of column does not match nodes_per_slice');
% node 1 = hidden node
% node 2:nodes_per_slice = observable nodes

users = unique(data(:,1)); % list of unique users
ncases = size(users,1); % number of unique users, also the number of cases

%% ------Outputs ------
% cases = 1 x number of cases
% each case is a slice size x number of slices cell

cases = cell(1,ncases);
%'supports' stores all states for each observable nodes by ordered by index
% e.g. if we have resource_id [23,344,1666], in bnet, they will be referenced
% by their index [1,2,3]
supports = cell(1,nodes_per_slice-1); 
% ------------------------

%% make empty answer a state 11
if (empty_state == 1)
    EMPTY_ANSWER = size(supports{2},1)+1;
    supports{2}(EMPTY_ANSWER) = 0;
end	

%% make answer binary
%fprintf('binary is %i',binary);
if (binary == 1)
    supports{2} = transpose(1:2);
end

%% make resource +1 support
if (empty_res == 1)
    EMPTY_RESOURCE = size(supports{1},1)+1;
    supports{1}(EMPTY_RESOURCE) = 0;
end

%%
%fill up all possible state for each node, excluding 0 = empty
for node=1:nodes_per_slice-1
    supports{node} = unique(data(data(:,node+1)~= 0 ,node+1));
end

%fill up cases
for u=1:ncases
	userdata = data(data(:,1) == users(u),:); %all lines of data related to this user
	
	cases{u} = cell(nodes_per_slice, max_num_of_slices);

	for slice = 1:min(size(userdata,1),max_num_of_slices)
        for node = 2:nodes_per_slice
            if (userdata(slice,node) ~= 0)
                cases{u}(node,slice) = num2cell(find(supports{node-1} == userdata(slice,node)));
            end

            %% make empty answer a last state for res node
            if (empty_res == 1)
                if (node == 2) && (userdata(slice,node) == 0)
                    cases{u}(node,slice) = num2cell(EMPTY_RESOURCE);
                end
            end
	    
            %% make empty answer a state 11
            if (empty_state == 1)
                if (node == 3) && (userdata(slice,node) == 0)
                    cases{u}(node,slice) = num2cell(EMPTY_ANSWER);
                end
            end
            
            %% make answers binary
            if (binary == 1)
                if (node == 3) && (userdata(slice,node) > 1)
                    cases{u}(node,slice) = num2cell(2);
                end
            end
        end        
	end
end	


