% cd into the directory where set_parameters.m for the task is located
cd 'C:\Users\Elaine\Documents\edx\dcap_test\tasks\testBnetTask'

dataDirectory = strcat(pwd);
resultDirectory = strcat(pwd,'/results');
addpath(genpath('C:\Users\Elaine\Documents\edx\dcap_test\bnet'));
%run_bnet(dataDirectory, resultDirectory);

warning off

	%add codebase to path
	cd(dataDirectory);

	%load the parameters
	set_parameters()
    
    %[result,~] = run_general_bnet_experiment(parameters);

	%RUN_BNET_EXPERIMENT Summary of this function goes here
    %  Trains a bnet
    

    %% Initialize result cell
    % result cell contains one struct for each cross validation run.
    result = {parameters.K};

    %% Load data, currently data format is problem specific except first column represents user_id
    input_folder = ('data\');
	addpath(genpath(input_folder));
    data =  load ([input_folder parameters.input_file]);
	intra = load ([input_folder parameters.intra_file]);
	inter = load ([input_folder parameters.inter_file]);

    % inter, intra matrix are matching square matrices, and use this to determine number of observable nodes
	assert(size(inter,1) == size(inter,2), 'inter matrix not a square matrix')
	assert(size(intra,1) == size(intra,2), 'intra matrix not a square matrix')
	assert(size(intra,1) == size(inter,1), 'intra inter matrices do not have matching dimensions')
    
    %% if want to remove resource id 2033 which corresponds to the problem 330 page
    %data = data(data(:,4) ~= 2033,:);
    size(data,1)
    
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
    max(length)
    max_num_of_slices = ceil(quantile(length,0.95))
	
	nodes_per_slice = size(inter,1);
	numberOfObservableNodes = nodes_per_slice-1;
	
    %for testing, reduce input size
    %data = data(1:3000,:);
    
    %% problem specific formatting into uniform format
    % user_id, observable node 1,  observable node 2, ....
    formatted_data = format_data_for_problems_csv(data, nodes_per_slice,parameters.pick_feature);
    % put into cases    
	[cases,supports] = format_data_into_cases(formatted_data, max_num_of_slices, nodes_per_slice,1,0);

    %% ------determine observable node support------ 
	observable_node_support = ones(1,numberOfObservableNodes);
    for node=1:numberOfObservableNodes
        observable_node_support(1,node) = size(supports{node},1);
    end
	
    %cases = cases(1,1:1000);
    %% Calculate cross-validation indices    
    N = size(cases,2);
%     indices = pick_indices(N, parameters.K, parameters.number_to_train, parameters.number_to_test);
%     save('indices','indices');
    load indices1000
    
    
    
    parameters.max_iterations = 1;
    [~] = build_general_DBNM(cases(1:2), parameters, max_num_of_slices, inter, intra, observable_node_support, 'dirichlet');
    parameters.max_iterations = 100;
    
%     launch_matlabpool(4);
%     
%     %% Train bnet
%     parfor crossvalidation_number = 1:parameters.K
%         tic;
%         fprintf('fold %i',crossvalidation_number);
%         data_train_idx = indices{crossvalidation_number}.data_train_idx;
%         data_test_idx = indices{crossvalidation_number}.data_test_idx;
%         data_train = cases(data_train_idx);
%         
% 
%         
%         [learnt_engine, loglik_trace,bnet] = build_general_DBNM(data_train, parameters, max_num_of_slices, inter, intra, observable_node_support, 'dirichlet');
%        
% 
%         
%         crossval_result = {};
%         crossval_result.learnt_engine = learnt_engine;
%         crossval_result.loglik_trace = loglik_trace;
%         crossval_result.data_train_idx = data_train_idx;
%         crossval_result.data_test_idx = data_test_idx;
%         result{crossvalidation_number} = crossval_result;
%         toc;
%        
%         
%     end
% 
%     matlabpool close
% 
%  
%     
%     
%     %         data_test = cases(data_test_idx);
%         
%         numTest = size(data_test,2);
%         test_loglik = zeros(1,numTest);
%         
%         test_engine = learnt_engine;
%         for u=1:numTest
%             [test_engine, loglik] = enter_evidence(test_engine,data_test{u});
%             test_loglik(u) = loglik;
%         end
            


    