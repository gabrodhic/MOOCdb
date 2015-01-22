'''
Generates set_parameters.m for bnet experiment
Please run from own directory!


Author: Colin Taylor (ALFA @ CSAIL)
Email: colin2328@gmail.com
Date: 8/6/2013 (creation)

Modified by: Elaine Han(skewlight@gmail.com)
Last modified: 4/10/2014
'''

import itertools
import os
import shutil


def create_dir_if_not_exists(directory):
    '''creates a directory if it does not exist with the full path name'''
    if not os.path.isdir(directory):
            os.makedirs(directory)

#parameters
hidden_node_support_list = [5,10,15,20,30]
data_list = ['problem_330_v2.csv']
DAG_list = ['1','2','3']
max_iterations = 100
feature_list = ['1','2']
number_to_train = 0
number_to_test = 0

generate_dir =  os.getcwd()
assert os.path.basename(generate_dir) == 'generateScripts', 'Script must be called from generateScripts directory!'
tasks_dir =  os.path.join(os.path.dirname(generate_dir), 'tasks')
assert os.path.isdir(tasks_dir), 'Tasks directory must be exist!'
os.chdir(tasks_dir)
tasks_file = open("generatedBnetTasks.txt", "w")

for data in data_list: #loop over data_list
    for dag in DAG_list:
        for support in hidden_node_support_list: #loop over hidden_node_support_list
            for feature in feature_list:
            # for each experiment:
                    
                # creates folder in tasks/ with the taskName
                folder_name = 'rBnet_DAG'+ str(dag)+ 'sup' + str(support) +'ite'+str(max_iterations)+'f'+feature
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
''' %(data, dag, dag, feature)

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
                os.chdir(tasks_dir)
                #break
        # 	break
        # break
tasks_file.close()





