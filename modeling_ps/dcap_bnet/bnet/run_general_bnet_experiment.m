%% Last modified: 5/21/2014
%% Author: Elaine Han (skewlight@gmail.com)

function [ result, supports, allfold_result, case_idx ] = run_general_bnet_experiment(parameters)
    % Train + test a bnet
    % 1) k-fold CV on training set
    % 2) for 'k+1-th' fold train on all training set + test on a separate testing set
    tic;

    %% Load data, currently data format is problem specific except first column represents user_id
    input_folder = ('data/');
	addpath(genpath(input_folder));
    data =  load ([input_folder parameters.input_file]);
	intra = load ([input_folder parameters.intra_file]);
	inter = load ([input_folder parameters.inter_file]);

    % inter, intra matrix are matching square matrices, and use this to determine number of observable nodes
	assert(size(inter,1) == size(inter,2), 'inter matrix not a square matrix')
	assert(size(intra,1) == size(intra,2), 'intra matrix not a square matrix')
	assert(size(intra,1) == size(inter,1), 'intra inter matrices do not have matching dimensions')
  
	%% ------determine max number of slices------
	users=unique(data(:,1)); %list of unique user id
    numberU = size(users,1);
    length = zeros(numberU,1);
	for i=1:numberU
        u = users(i);
		max_ue = sum(data(:,1) == u);
        length(i) = max_ue;

	end
	% -------------------------------------
    max_num_of_slices = ceil(quantile(length,0.95)); % handle huge outliers, change bound accordingly

	nodes_per_slice = size(inter,1);
	numberOfObservableNodes = nodes_per_slice-1;
	
    
    %% problem specific formatting into uniform format
    % user_id, observable node 1,  observable node 2, ....
    formatted_data = format_data_for_problems_csv(data, nodes_per_slice,parameters.pick_feature);
    % put into cases
	[cases,supports] = format_data_into_cases(formatted_data, max_num_of_slices, nodes_per_slice,parameters.empty_state,parameters.empty_res,parameters.binary);

    %% ------determine observable node support------ 
	observable_node_support = ones(1,numberOfObservableNodes);
    for node=1:numberOfObservableNodes
        observable_node_support(1,node) = size(supports{node},1);
    end

    if (parameters.idx == 1) %use saved indicies
        load([input_folder 'fold_idx.mat']);
        load([input_folder 'case_idx.mat']);
        load([input_folder 'final_test_idx.mat']);
    else
        %%  take parameters.ncases cases randomly, save the case idx used
        totalcases = size(cases,2); %total cases we pick from
        to_pick = min(parameters.ncases,totalcases);
        case_idx = transpose(randsample(totalcases,to_pick,false));
        final_test_idx = transpose(randsample(totalcases,to_pick,false)); %TODO: PLACE HOLDER ! need to take another ? different cases from case_idx!!!
    end
    
    final_test = cases(final_test_idx); %testing set
    cases = cases(case_idx); %training set

    %% Initialize result cell
    % result cell contains one struct for each of k fold CV and one more for training on all training set.
    result = cell(1,parameters.K+1);
    
    %% Initialize result cell for cv predictions
    % allfold_result contains predictiong for each of k fold CV and one more for testing on all testing set.
    allfold_result = cell(1,parameters.K+1);
	
    %% Calculate cross-validation indices    
    N = size(cases,2);
    launch_matlabpool(parameters.number_of_threads+1);
    %use saved fold indices or generate new
    if (parameters.idx==1)
        indices = fold_idx;
    else
        indices = pick_indices(N, parameters.K, parameters.number_to_train, parameters.number_to_test);
    end
    indices{parameters.K+1} = []; %must set this else parfor give exceeds dimension error
    
    % small run to set up, else saved result objects lose the bnt engine class
    fprintf('Set up short test run');
    [~] = build_general_DBNM(cases(1:2),parameters,max_num_of_slices, inter,intra,observable_node_support,'dirichlet');
  
    %% Training bnet
    parfor crossvalidation_number=1:parameters.K+1
        fprintf('\n%i\n',crossvalidation_number);
        if (crossvalidation_number<parameters.K+1)
            data_train_idx = indices{crossvalidation_number}.data_train_idx;
            data_test_idx = indices{crossvalidation_number}.data_test_idx;
	   
            data_train = cases(data_train_idx);
        else %for last fold where we train on all data
            data_train_idx = 1:N;
            data_test_idx = final_test_idx;
            data_train = cases;
        end

        [bnet,learnt_engine, loglik_trace] = build_general_DBNM(data_train, parameters, max_num_of_slices, inter, intra, observable_node_support, 'dirichlet');
        
        crossval_result = {};
        crossval_result.bnet = bnet;	
        crossval_result.learnt_engine = learnt_engine;
        crossval_result.loglik_trace = loglik_trace;
        crossval_result.data_train_idx = data_train_idx;
        crossval_result.data_test_idx = data_test_idx;
        result{crossvalidation_number} = crossval_result;

	%% Running predictions
        
        engine = learnt_engine;
        if (crossvalidation_number<parameters.K+1)
            data_test = cases(data_test_idx);
        else
            data_test = final_test; %final testing set
        end
        ncases = size(data_test,2); %number of test cases, aka, number of users       
        ecases = cell(1,ncases); %create empty cases to fill in each time slice
        
        predresult = {}; %a structure to put all the predictions in
        pred = [];
        hidden_state = [];
		
        %1) if current slice contains non-empty (not a []) answer node
        %(node=3) look at the marginal prob for it

        node = 3;
        predresult.node = node;
		
        fprintf('number of test cases: %i',ncases);

        for u=1:ncases
            ecases{u} = cell(nodes_per_slice, max_num_of_slices);
            if (mod(u,100) ==0)
                fprintf('case %i/%i\n',u,ncases);
            end
            
            for slice=1:max_num_of_slices
               	% if this slice is empty, end this case, go to next case
                if (isEmptySlice(data_test{u}(:,slice)))
                    break
                end
                
                %for each slice, first enter previous slices as evidence
                [engine,ll] = enter_evidence(engine, ecases{u});
                
                % PREDICTIONS
                %1) if current slice contains non-empty (not a []) answer node
                %(node=3) look at the marginal prob for all possible states
                %pred = [user, actual_value, marg for all values]
             	
                if ~(isempty(data_test{u}{node,slice}))
                    marg = marginal_nodes(engine, node, slice);
                    pred = [pred; u data_test{u}{node,slice} transpose(marg.T)];
                end
               
                %fill in ecases to be used for enter_evidence of next slice
                ecases{u}(:,slice) = data_test{u}(:,slice);
            end
            
            		% 2) marg of hidden state at the end for each user case
            hnode = 1;
            margh = marginal_nodes(engine, hnode, slice);
            
            %each row of prediction is [ user_indicator marginal_prob]
            hidden_state = [hidden_state; u transpose(margh.T)]; 
            
        end
        predresult.pred = pred;
        predresult.hidden_state = hidden_state;        
        allfold_result{crossvalidation_number} = predresult;	
    end
    
    matlabpool close
    toc;
end

