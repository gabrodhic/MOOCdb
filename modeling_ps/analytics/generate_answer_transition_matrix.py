"""
    Elaine Han (skewlight@gmail.com)
    created 5/13/2014

    Generate answer transition matrix for top unique anwers.
"""

import csv
import os
from os import listdir
from os.path import isfile, join


CSV_FOLDER_PATH = "problem_csv_v2/"
COUNT_FOLDER_PATH = "problem_resource_count/"

USER_INDEX = 0
ANSWER_INDEX = -1
RESOURCE_INDEX = 2
EMPTY_ANSWER = 0
FILE_NAME = "problem_%i_v2.csv"
OUTPUT_FOLDER = "answer_transition/"

unique = 10 #number of top unique answers excluding empty

def answer_transition_matrix(problem_id):
    print "Problem: %i"%problem_id

    filename = os.path.join(CSV_FOLDER_PATH, FILE_NAME%problem_id)

    matrix = [[0]*unique for i in range(unique)]

    usercount = 0
    answercount = [0]*10
    answeruser = [[] for i in range(unique)]
        
    with open(filename,'r') as csvfile:
        reader = csv.reader(csvfile)

        user = None #current user
        prev = None #previous answer
        prevrow = None

        count = 0
        for row in reader:
            if float(row[ANSWER_INDEX]) != EMPTY_ANSWER: #is submission event
                ans = int(float(row[ANSWER_INDEX]))
                answercount[ans-1] +=1
                if row[0] not in answeruser[ans-1]:
                    answeruser[ans-1].append(row[0])
                    
                    
                if row[0] != user:
                    usercount += 1
                    user = row[0]
                    prev = ans
                    prevrow = row
                else: #same user as previous event
                    if prev == ans and count<100:
                        #print prevrow
                        #print row
                        #print " "
                        count += 1
                    matrix[prev-1][ans-1] += 1
                    prev = ans
                    prevrow = row
    print "Total student: %i"%usercount
    print "Answer "+"%6i| "*unique%tuple(range(1,11))
    print "Count  "+"%6i| "*unique%tuple(answercount)
    print "User   "+"%6i| "*unique%tuple([len(answeruser[i]) for i in range(10)])
    print " "
##    for i in matrix:
##        print i
    return matrix
    


if __name__ == "__main__":
    
    problem_list = [94,111,121,135,139,161,181,183,229,236,239,259,276,318,326,\
                    330,332,353,358,369,467,479,484,513]
    problem_list = [111,121,135,229,236,239,369,467,513]
    for problem in problem_list:
        matrix = answer_transition_matrix(problem)

##        filename = os.path.join(OUTPUT_FOLDER,"answer_transition_%i.csv"%problem)
##        with open(filename,'w') as csvfile:
##            writer = csv.writer(csvfile)
##            for row in matrix:
##                writer.writerow(row)

