'''
Generates set_parameters.m for bnet experiment
Please run from own directory!


Created by: Elaine Han(skewlight@gmail.com)
Created on: 5/9/2014

Data files (extracted trajectories and inter/intra csv files) should
be located in this directory (/generateScripts) to be copied into
task folders under /tasks. Alternatively the paths to intput data files 
could be modified to access data in subfolders.
'''

import itertools
import os
import shutil


def create_dir_if_not_exists(directory):
    '''creates a directory if it does not exist with the full path name'''
    if not os.path.isdir(directory):
            os.makedirs(directory)

#parameters
hidden_node_support_list = [10,15,20,30]
problem_list= [94,111,121,135,139,161,181,183,229,236,239,259,276,318,326,\
                    330,332,353,358,369,467,479,484,513]
DAG_list = ['1','4']
max_iterations = 100
feature_list = ['1']
number_to_train = 0
number_to_test = 0
empty_state = 1
empty_res = 0
binary = 0 #either 1= use binary or 0=use answer types

# Indices could be loaded to make sure that different models
# use the exact same train and test samples for each problem.
idx = 1 #1 = use save indices, 0 = generate new
idx_dir = 'indices_problem-short24'

generate_dir =  os.getcwd()
assert os.path.basename(generate_dir) == 'generateScripts', 'Script must be called from generateScripts directory!'
tasks_dir =  os.path.join(os.path.dirname(generate_dir), 'tasks')
assert os.path.isdir(tasks_dir), 'Tasks directory must be exist!'
os.chdir(tasks_dir)

tasks_file = open("exampleBnetTasks.txt", "w")

for problem_id in problem_list: #loop over data_list
    data = "problem_%i_v2_filtered_combine.csv"%problem_id
    for dag in DAG_list:
        for support in hidden_node_support_list: #loop over hidden_node_support_list
            for feature in feature_list:
            # for each experiment:
                    
                # creates folder in tasks/ with the taskName
                folder_name = 'problem_%i_DAG'%problem_id+ str(dag)+ 'sup' + str(support)
		#folder_name = 'problem_%i_HMM_binary_sup10'%problem_id
                create_dir_if_not_exists(folder_name)

                # adds set_parameters.m to folder
                fo = open(folder_name + "/set_parameters.m", "w")


                input_parameters = '''
%% Input parametes
parameters = struct;

parameters.input_file = \'%s\';
parameters.inter_file = \'inter_%s.csv\';
parameters.intra_file = \'intra_%s.csv\';
parameters.pick_feature = %s;
parameters.empty_state = %i;
parameters.empty_res = %i;
parameters.ncases = 1000;
parameters.idx = %i;
parameters.binary = %i;
''' %(data, dag, dag, feature, empty_state,empty_res,idx,binary)

                cross_validation_parameters = '''
%% Cross validation parameters
parameters.number_to_train = %s;             %% 0 for full cross validation
parameters.number_to_test = %s;              %% 0 for full cross validation
parameters.K = 5;                          %% Number of cross validations.
parameters.number_of_threads = parameters.K;          %% It's a good idea to choose number_of_threads == K
''' %(number_to_train, number_to_test)

                bnet_learning_parameters = '''
%% BNET learning parameters
parameters.hidden_node_support = %s;
parameters.max_iterations = %i;
parameters.stopping_condition = 1e-3;
parameters.train_anneal_rate = 0.8;
''' %(str(support),max_iterations)

                # populates set_parameters.m
                fo.write( input_parameters);
                fo.write( cross_validation_parameters);
                fo.write( bnet_learning_parameters);
                fo.close()

                # concatanates a row to bnetTasks with a name, path to py, and folder
                task = '%s,../tasks/run_bnet.py,../tasks/%s\n' %(folder_name, folder_name)
                tasks_file.write(task)

                #copy data
                data_dir = os.path.join(tasks_dir,folder_name,'data')
                create_dir_if_not_exists(data_dir)
                os.chdir(data_dir)
                shutil.copy(os.path.join(generate_dir, data),data_dir)
                shutil.copy(os.path.join(generate_dir, 'intra_'+dag+'.csv'),data_dir)
                shutil.copy(os.path.join(generate_dir, 'inter_'+dag+'.csv'),data_dir)
		
		if idx==1:
			shutil.copyfile(os.path.join(generate_dir,idx_dir,'problem_%i_fold_idx.mat'%problem_id),os.path.join(data_dir,'fold_idx.mat'))
			shutil.copyfile(os.path.join(generate_dir,idx_dir,'problem_%i_case_idx.mat'%problem_id),os.path.join(data_dir,'case_idx.mat'))
			shutil.copyfile(os.path.join(generate_dir,idx_dir,'problem_%i_final_test_idx.mat'%problem_id),os.path.join(data_dir,'final_test_idx.mat'))


                os.chdir(tasks_dir)
                #break
        # 	break
        # break
tasks_file.close()





