function [bnet,learnt_engine, loglik_trace]=build_general_DBNM(cases, parameters, max_num_of_slices,inter_matrix, intra_matrix, observableNodeSupport, priorType)

% Search to import bnt
if exist('bnt', 'dir')
    addpath(genpath('bnt'));
else
    error('Cannot find BNT folder')
end


%% ------additional assertions------
assert(parameters.max_iterations > 0 && parameters.max_iterations == floor(parameters.max_iterations), 'max_iterations must be an integer > 0')
assert(parameters.hidden_node_support > 0 && parameters.hidden_node_support == floor(parameters.hidden_node_support), 'hidden_node_support must be an integer > 0')

%BNT toolbox does not support discrete values of zero
%for i = 1:length(data)
%    assert(sum(sum(data{i}==0)) == 0,'BNT toolbox does not support discrete values of zero');
%end

% inter, intra matrix are matching square matrices, and use this to determine number of observable nodes
assert(size(inter_matrix,1) == size(inter_matrix,2), 'inter matrix not a square matrix')
assert(size(intra_matrix,1) == size(intra_matrix,2), 'intra matrix not a square matrix')
assert(size(intra_matrix,1) == size(inter_matrix,1), 'intra inter matrices do not have matching dimensions')

nodes_per_slice = size(inter_matrix,1);
numberOfObservableNodes = nodes_per_slice-1;
%----------------------------------



%% ------define nodes------
dnodes = 1:nodes_per_slice;

%% ------ node support-----
% hidden: parameters.hidden_node_support
% observable: observableNodeSupport

assert(length(observableNodeSupport) == numberOfObservableNodes);
support_for_each_node = [parameters.hidden_node_support observableNodeSupport];

%% ------equivalence class------
eclass_first_time_slice=1:nodes_per_slice;
eclass_second_time_slice=[1:nodes_per_slice]+nodes_per_slice;  %from third time slice onwards it uses the same eclass as second
all_eclass=[eclass_first_time_slice eclass_second_time_slice];
% ------------------------------


%% ------DAG given by input inter_matrix, intra_matrix------


bnet = mk_dbn(intra_matrix, inter_matrix, support_for_each_node, 'discrete', dnodes, ...
    'eclass1', eclass_first_time_slice, 'eclass2', eclass_second_time_slice);

	
%% ------setting initial parameters for each eclass------
% if node has no parent, the initial parameter is of dimension node support x 1
%			has parents, dimension is parent_1 support x parent_2 support ... x node support

for n=all_eclass
   
	param_dimension = [];
	if (n > nodes_per_slice)
        temp_n = n-nodes_per_slice;
    else
        temp_n = n;
    end
	% first slice class, only depend on intra edges if any
	for p=1:nodes_per_slice
		if (intra_matrix(p,temp_n) == 1)
			param_dimension = [param_dimension support_for_each_node(p)];
		end
	end
	
	% second slice class, depend on both intra+inter edges if any
	if (n > nodes_per_slice)
		for p=1:nodes_per_slice
			if (inter_matrix(p,temp_n) == 1)
				param_dimension = [param_dimension support_for_each_node(p)];
			end
		end
	end
	
	if (size(param_dimension,2)==0)
		param = mk_stochastic(rand(support_for_each_node(temp_n),1));
    else

		param = mk_stochastic(rand([param_dimension support_for_each_node(temp_n)]));

    end
	
    
	bnet.CPD{n} = tabular_CPD(bnet,n,param,'prior_type',priorType);
end



% Here you are specifying the engine and putting the BNT in it. 
% Note: http://bnt.googlecode.com/svn/trunk/docs/usage_dbn.html:
% "If all the hidden nodes are discrete, we can use the junction tree algorithm to perform inference"
engine = jtree_unrolled_dbn_inf_engine(bnet,max_num_of_slices);



[bnet, loglik_trace, learnt_engine] = learn_params_dbn_em(engine, cases, 'max_iter', parameters.max_iterations);
	


