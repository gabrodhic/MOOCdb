% Last modified: 5/21/2014
% Author: Elaine Han (skewlight@gmail.com)

%% Train and test a bnet model.
% output result contains trained models for k+1 folds which:
% 1) first k folds are for each fold of the k-fold CV on
%    training set.
% 2) for the 'k+1-th' fold, train on the whole training set.
%    The result is for testing on a separate testing set.
%
% allfold_result stores the predictions for the k+1 folds.
function [ result, supports, allfold_result, case_idx ] = run_general_bnet_experiment(parameters)
 
    tic;

    %% Load data, currently data format is problem specific except the first column which will always represent user_id.
    input_folder = ('data/');
	addpath(genpath(input_folder));
    data =  load ([input_folder parameters.input_file]);
	intra = load ([input_folder parameters.intra_file]);
	inter = load ([input_folder parameters.inter_file]);

    % inter, intra matrix are matching square matrices. Using size of those
    % matrices to determine number of observable nodes.
	assert(size(inter,1) == size(inter,2), 'inter matrix not a square matrix')
	assert(size(intra,1) == size(intra,2), 'intra matrix not a square matrix')
	assert(size(intra,1) == size(inter,1), 'intra inter matrices do not have matching dimensions')
  
	%% ------determine max number of slices------
    % which is the longest event sequence that we will have.
	users=unique(data(:,1)); %list of unique user id
    numberU = size(users,1);
    length = zeros(numberU,1);
	for i=1:numberU
        u = users(i);
		max_ue = sum(data(:,1) == u);
        length(i) = max_ue;
    end
    % handle huge outliers, change quantile accordingly.
    max_num_of_slices = ceil(quantile(length,0.95)); 
    % -------------------------------------
	nodes_per_slice = size(inter,1);
	numberOfObservableNodes = nodes_per_slice-1;
	    
    %% problem specific formatting into uniform format
    % For problem solving model, the formatted data is in format:
    %   user_id, observable node 1,  observable node 2
    formatted_data = format_data_for_problems_csv(data, nodes_per_slice, parameters.pick_feature);
    % put into cases
	[cases, supports] = format_data_into_cases(formatted_data, max_num_of_slices, nodes_per_slice, parameters.empty_state, parameters.empty_res, parameters.binary);

    %% ------determine observable node support------ 
    % which is the number of possible states for each node
	observable_node_support = ones(1, numberOfObservableNodes);
    for node=1:numberOfObservableNodes
        observable_node_support(1, node) = size(supports{node},1);
    end
    
    %% Getting training set (to perform CV on) and final testing set.
    % When parameters.idx is 1, use saved indicies to make sure that
    % different runs will be training/testing on the exact same cases.
    % TODO: check if those files actually exist.
    if (parameters.idx == 1) % use saved indicies
        load([input_folder 'fold_idx.mat']);
        load([input_folder 'case_idx.mat']);
        load([input_folder 'final_test_idx.mat']);
    else
        % take parameters.ncases cases randomly, save the case idx used
        totalcases = size(cases,2); %total number of cases we can pick from
        to_pick = min(parameters.ncases, totalcases);
        case_idx = transpose(randsample(totalcases, to_pick, false));
        % TODO: The final_test_idx should be non-overlapping with case_idx.
        % Also currently we are picking same number of indexes for each
        % set. We might want to set different numbers.
        final_test_idx = transpose(randsample(totalcases, to_pick, false)); 
    end
    
    % Training and testing set
    final_test = cases(final_test_idx); % final testing set for k+1-th fold
    cases = cases(case_idx); % training set to perform k-fold CV on

    %% Initialize result cell
    % result cell contains one struct for each of k fold CV and 
    % one more struct for training on all training set.
    result = cell(1,parameters.K+1);
    
    %% Initialize allfold_result cell for storing cv predictions
    % allfold_result contains predictions for each of k fold CV and
    % one more for testing on all testing set.
    allfold_result = cell(1,parameters.K+1);
	
    %% Calculate cross-validation indices    
    N = size(cases,2);
    launch_matlabpool(parameters.number_of_threads+1);
    % use saved fold indices or generate new
    if (parameters.idx==1)
        indices = fold_idx;
    else
        indices = pick_indices(N, parameters.K, parameters.number_to_train, parameters.number_to_test);
    end
    indices{parameters.K+1} = []; %must set this else parfor give exceeds dimension error
    
    % small run to set up, else saved result objects lose the bnt engine class
    fprintf('Set up short run to work around an error.\n');
    [~] = build_general_DBNM(cases(1:2),parameters,max_num_of_slices, inter,intra,observable_node_support,'dirichlet');
    fprintf('Short run done.\n');
    %% Training bnet
    parfor crossvalidation_number=1:parameters.K+1
        fprintf('\n%i\n',crossvalidation_number);
        % first k folds
        if (crossvalidation_number  <parameters.K+1)
            data_train_idx = indices{crossvalidation_number}.data_train_idx;
            data_test_idx = indices{crossvalidation_number}.data_test_idx;	   
            data_train = cases(data_train_idx);
        else % for last fold where we train on all data
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
        if (crossvalidation_number < parameters.K+1)
            data_test = cases(data_test_idx); % first k-fold
        else
            data_test = final_test; % final testing set
        end
        
        ncases = size(data_test,2); % number of test cases, aka, number of users       
        ecases = cell(1,ncases); % create empty cases to fill in each time slice
        
        predresult = {}; %a structure to put all the predictions in
        pred = [];
        hidden_state = [];
		
        % answer node (node=3)
        node = 3;
        predresult.node = node;
		
        fprintf('Predicting number of test cases: %i\n',ncases);

        for u=1:ncases
            ecases{u} = cell(nodes_per_slice, max_num_of_slices);
            % print status every 100 cases.
            if (mod(u,100) ==0)
                fprintf('Case %i/%i\n',u, ncases);
            end
            
            for slice=1:max_num_of_slices
               	% if this slice is empty, end this case, go to next case
                if (isEmptySlice(data_test{u}(:,slice)))
                    break
                end
                
                %for each slice, first enter previous slices as evidence
                [engine,ll] = enter_evidence(engine, ecases{u});
                
                % PREDICTIONS
                % 1) if current slice contains non-empty (not a []) answer node
                % (node=3) look at the marginal prob for all possible states
                % pred = [user, actual_value, marg for all other states]
             	
                if ~(isempty(data_test{u}{node,slice}))
                    marg = marginal_nodes(engine, node, slice);
                    pred = [pred; u data_test{u}{node,slice} transpose(marg.T)];
                end
               
                % fill in ecases to be used for enter_evidence of next slice
                ecases{u}(:,slice) = data_test{u}(:,slice);
            end
            
            % 2) marg for states of hidden node at the end for each user case
            hnode = 1;
            margh = marginal_nodes(engine, hnode, slice);
            hidden_state = [hidden_state; u transpose(margh.T)]; 
            
        end
        predresult.pred = pred;
        predresult.hidden_state = hidden_state;        
        allfold_result{crossvalidation_number} = predresult;	
    end
    
    matlabpool close
    toc;
end

