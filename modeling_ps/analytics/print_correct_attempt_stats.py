"""
    Elaine Han (skewlight@gmail.com)
    Created 1/22/2014
    
    To look at, for each problem:
        1. how many students get correct on 1st try, 2nd, etc...
        2. changing from correct to incorrect answer
    either from old* csv files

    print list of attempt number, % and count of students who first got the problem right on this attempt

    USING OLD CSV FILE FORMAT
    To use with other versions of student trajectory csv files, indexes must be modified to fit the columns.
"""


import csv
import os


CSV_FOLDER_PATH = "problem_csv_old_sample/" #old csv files

def correct_attempt_stats_from_csv(problem_id):
    
    ########################################
    ######### from old csv files ###########
    ########################################
    
    filename = os.path.join(CSV_FOLDER_PATH, "Problem_%i.csv"%problem_id) 

    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)

        
        user_count = 0 #total user count for this problem
        user_id = None #user id we looking at        
        attempt_number = 0 #which attempt we are on
        user_correct = 0 # 0=incorrect, 1=correct, 2=correct to incorrect 
        
        attempt_dict = {} #store correct attempt stats

        correct_to_in = 0 #incorrect after correct 
        correct_after_c = 0 # correct after correct 
        
        for row in reader:
            if float(row[-1]) != 2.0: # is a submission event              

                row_user_id = int(row[0])

                #re-initialize for every new user
                if user_id != row_user_id:
                    user_id = row_user_id
                    attempt_number = 0
                    user_correct = 0
                    user_count += 1

                attempt_number += 1

                # first correct attempt
                if float(row[-1]) == 1.0 and user_correct == 0 : 
                    if attempt_number in attempt_dict:
                        attempt_dict[attempt_number] += 1
                    else:
                        attempt_dict[attempt_number] = 1
                    user_correct = 1
                    
                # incorrect attempt(s) after correct, count once for same user
                elif float(row[-1]) == 0.0 and user_correct == 1:
                    correect_to_in += 1
                    user_correct = 2

                # correct attempt(s) after correct, count once for same user
                elif float(row[-1]) == 1.0 and user_correct == 1:
                    correct_after_c += 1


    return (attempt_dict,correct_to_in,correct_after_c,user_count)

if __name__ == "__main__":
    
    problem_list = [174,253,330]
    for problem in problem_list:
        print "Problem ID: %i"%problem
        (attempt_dict,correct_to_in,correct_after_c,user_count) = correct_attempt_stats_from_csv(problem)
        print "Total student count: %i, Incorrect after correct: %i, Correct after correct: %i"%(user_count,correct_to_in,correct_after_c)
        for i in range(1,6):
            print "%3i: %.2f%%, %i"%(i,100*attempt_dict[i]/float(user_count),attempt_dict[i]) #including incorrect
        print "Incorrect: %.2f%%"%(100*(1-(sum(attempt_dict.values())/float(user_count))))

                


                

                
            



















            
            
