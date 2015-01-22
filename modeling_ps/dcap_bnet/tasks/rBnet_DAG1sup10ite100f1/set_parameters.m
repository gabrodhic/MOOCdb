
% Input parametes
parameters = struct;

parameters.input_file = 'problem_330_v2.csv';
parameters.inter_file = 'inter_1.csv';
parameters.intra_file = 'intra_1.csv';

% Cross validation parameters
parameters.number_to_train = 0;             % 0 for full cross validation
parameters.number_to_test = 0;              % 0 for full cross validation
parameters.K = 5;                          % Number of cross validations.
parameters.number_of_threads = parameters.K;          % It's a good idea to choose number_of_threads == K

% BNET learning parameters
parameters.hidden_node_support = 10;
parameters.max_iterations = 100;
parameters.stopping_condition = 1e-3;
parameters.train_anneal_rate = 0.8;
