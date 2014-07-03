"""
    Created on: 5/24/2014
    Author: Elaine Han (skewlight@gmail.com)
"""

import csv
from os.path import join

problem_list= [330]


CSV_FOLDER_PATH = "problem_csv_v2_filtered/"
CSV_FOLDER_PATH = "problem_csv_v2/"
OUTPUT_FOLDER = "answer_type_count/"
FILE_NAME = "problem_%i_v2_filtered_combine.csv"
FILE_NAME = "problem_%i_v2.csv"

USER_INDEX = 0
ANSWER_INDEX = -1
RESOURCE_INDEX = 2
EMPTY_ANSWER = 0


def count_answer_type(problem_id):
    """count 1) frequency of each answer type
             2) total number of events(both submission and observation) for all users who have answered this problem
             3) total number of students"""   
    filename = join(CSV_FOLDER_PATH, FILE_NAME%problem_id)
    count = [0 for i in range(11)]
    
    total_lines = 0
    users = []

    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            total_lines += 1
            if row[USER_INDEX] not in users:
                users.append(row[USER_INDEX])
                
            answer_type = int(float(row[ANSWER_INDEX]))
            #print answer_type
            count[answer_type] += 1

    return count, total_lines,users

if __name__ == "__main__":

    total = []
    problem_list = [330]
    for problem in problem_list:
        (count, total_lines,users) = count_answer_type(problem)
        total.append([problem]+count[1:]+[count[0]])
        print problem, count, total_lines

##    ## save to file
##    filename = "answer_type_count_24problems.csv"   
##    with open(filename,'w') as csvfile:
##        writer = csv.writer(csvfile)
##        for row in total:
##            writer.writerow(row)
        
